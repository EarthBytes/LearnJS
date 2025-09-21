from data import js_facts, conversation_prompts, user_status_responses, topic_synonyms, question_patterns
from memory import Memory
import re
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
import difflib
from examples import get_example
from sentence_transformers import SentenceTransformer, util

CONFUSED_INPUTS = {"huh?", "what?", "?", "idk", "i don't understand", "explain", "can you repeat?"}
NONSENSE_THRESHOLD = 0.3  # Minimum ratio of meaningful words to total words

class QuestionType(Enum):
    DEFINITION = "definition"
    EXAMPLE = "example"
    HOW_TO = "how_to"
    COMPARISON = "comparison"
    TROUBLESHOOTING = "troubleshooting"
    GENERAL = "general"

@dataclass
class Intent:
    topic: str
    question_type: QuestionType
    confidence: float

@dataclass
class Match:
    text: str
    response: str
    priority: int
    length: int  # Length of the matched phrase

class LearnJSBot:
    def __init__(self):
        self.memory = Memory(max_turns=5)
        
        # Import all data from data.py
        self.js_facts = js_facts
        self.prompts = conversation_prompts
        self.status_responses = user_status_responses
        self.synonyms = topic_synonyms
        self.patterns = question_patterns
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Precompute embeddings for JS facts
        self.fact_embeddings = {k: self.model.encode(v) for k, v in self.js_facts.items()}

    def get_response(self, user_input: str) -> str:
        # Main entry point for processing user input
        original = user_input
        normalized = user_input.lower().strip()
        
        # Handle yes/no follow-ups before storing user input
        followup_response = self._handle_followup(normalized)
        if followup_response:
            # Store the user input and return the followup response
            self.memory.store_turn("user", normalized)
            return followup_response
        
        # Store user input for all other cases
        self.memory.store_turn("user", normalized)
        
        # Early exits for special cases
        if self._is_nonsense(normalized):
            return self._store_and_return("I'm not sure what you're asking. Try asking about JavaScript concepts like variables, functions, or arrays!")
            
        # Handle status responses (after "how are you?")
        status_response = self._handle_status_response(normalized)
        if status_response:
            return status_response
        
        # Find conversation matches and learning intent
        conv_matches = self._find_conversation_matches(normalized)
        intent = self._extract_intent(original)
        
        # Generate response and get topic
        response, topic = self._generate_response(conv_matches, intent, original)
        
        # Clean multi-topic strings
        if topic and ':' in topic:
            topic = topic.split(':')[0]
            
        return self._store_and_return(response, topic)
    
    def _store_and_return(self, response: str, topic: str = None) -> str:
        # Helper to store bot response and return it
        self.memory.store_turn("bot", response, topic=topic)
        return response
    
    def _is_nonsense(self, text: str) -> bool:
        # Check if input is mostly nonsense
        if not text or len(text.split()) == 0:
            return True
            
        words = text.split()
        meaningful = sum(1 for word in words if self._is_meaningful_word(word))
        
        return meaningful / len(words) < NONSENSE_THRESHOLD
    
    def _is_meaningful_word(self, word: str) -> bool:
        # Check if a word is meaningful in context
        # Check against synonyms
        for synonyms in self.synonyms.values():
            if any(word in synonym.lower() for synonym in synonyms):
                return True
                
        # Check against prompts
        if any(word in prompt.lower() for prompt in self.prompts.keys()):
            return True
            
        # Common English words
        common_words = {
            'the','a','an','and','or','but','in','on','at','to','for','of','with','by',
            'is','are','was','were','be','been','have','has','had','do','does','did',
            'will','would','could','should','may','might','can','what','how','when','where','why',
            'who','which','this','that','these','those','i','you','he','she','it','we','they',
            'me','him','her','us','them'
        }
        return word in common_words
    
    def _handle_status_response(self, user_input: str) -> Optional[str]:
        # Handle responses to 'how are you' questions
        last_bot = self.memory.get_last_bot_turn()
        if not last_bot:
            return None
            
        if any(phrase in last_bot["text"].lower() for phrase in ["how are you", "how's it going", "how are you doing"]):
            for status, data in self.status_responses.items():
                if status in user_input:
                    return self._store_and_return(data["response"])
        return None
    
    def _handle_followup(self, user_input: str) -> Optional[str]:
        # check for follow-up yes/no
        last_bot = self.memory.get_last_bot_turn()
        last_topic = self.memory.get_last_topic()
        
        if not (last_bot and last_topic):
            return None
            
        # Check if bot asked for example or more explanation
        bot_text = last_bot["text"]
        asking_for_example = any(phrase in bot_text for phrase in [
            "Would you like to see an example?",
            "Want me to explain more?",
            "Need help with a specific use case?",
            "Want me to explain any part in more detail?"
        ])
        
        if not asking_for_example:
            return None
            
        user_input = user_input.strip()
        
        if user_input in ["yes", "y"]:
            example = get_example(last_topic)
            return self._store_and_return(example, last_topic)
        elif user_input in ["no", "n"]:
            return self._store_and_return("No problem! Ask me about another JavaScript topic.")
        else:
            return self._store_and_return("Please reply 'yes' or 'no'.")
    
    def _find_conversation_matches(self, text: str) -> List[Match]:
        # Find matching conversation prompts
        matches = []
        normalized = self._normalize_text(text)
        
        for prompt, data in self.prompts.items():
            # Direct match
            if prompt in text:
                pos = text.find(prompt)
                matches.append(Match(prompt, data['response'], data['priority'], len(prompt)))
            
            # Normalised match (avoid duplicates)
            norm_prompt = self._normalize_text(prompt)
            if norm_prompt in normalized and not any(m.text == prompt for m in matches):
                matches.append(Match(prompt, data['response'], data['priority'], len(norm_prompt)))
        
        # Sort by priority (desc), length (desc), then position (asc)
        return sorted(matches, key=lambda x: (-x.priority, -x.length))
    
    def _normalize_text(self, text: str) -> str:
        normalized = re.sub(r"[^\w\s]", "", text.lower())
        return re.sub(r"\s+", " ", normalized).strip()
    
    def _extract_intent(self, user_input: str) -> Intent:
        text_lower = user_input.lower()
        
        # Find topic matches
        topic_matches = self._find_topic_matches(text_lower)
        question_type = self._get_question_type(user_input)
        
        if not topic_matches:
            return Intent(None, question_type, 0.1)
        
        if len(topic_matches) > 1:
            topics = [match['topic'] for match in topic_matches]
            return Intent(f"multiple:{','.join(topics)}", question_type, 0.8)
        
        match = topic_matches[0]
        confidence = self._calculate_confidence(match, question_type, user_input)
        return Intent(match['topic'], question_type, confidence)
    
    def _find_topic_matches(self, text: str) -> List[Dict]:
        # Find all topic matches in text
        matches = []
        
        # Check synonyms first
        for topic, synonyms in self.synonyms.items():
            for synonym in synonyms:
                if synonym in text:
                    matches.append({
                        'topic': topic,
                        'keyword': synonym,
                        'position': text.find(synonym),
                        'confidence': 1.0
                    })
        
        # Also check your original js_facts keys
        for keyword in self.js_facts.keys():
            if keyword.lower() in text:
                mapped_topic = self._map_keyword_to_topic(keyword) or keyword
                if not any(m['topic'] == mapped_topic for m in matches):
                    matches.append({
                        'topic': mapped_topic,
                        'keyword': keyword,
                        'position': text.find(keyword.lower()),
                        'confidence': 1.0
                    })
        
        # Remove duplicates and sort
        unique_matches = []
        seen_topics = set()
        for match in sorted(matches, key=lambda x: (-x['confidence'], x['position'])):
            if match['topic'] not in seen_topics:
                unique_matches.append(match)
                seen_topics.add(match['topic'])
        
        return unique_matches
    
    def _get_question_type(self, text: str) -> QuestionType:
        # Determine question type from patterns
        text_lower = text.lower()
        type_scores = defaultdict(int)
        
        for q_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                if matches:
                    type_scores[q_type] += matches
        
        # Special handling for troubleshooting
        troubleshooting_words = ['error', 'issue', 'problem', 'not working', 'fix', 'debug', 'broken', 'wrong']
        if any(word in text_lower for word in troubleshooting_words):
            type_scores['troubleshooting'] += 2
        
        if not type_scores:
            return QuestionType.GENERAL
        
        best_type = max(type_scores.items(), key=lambda x: x[1])[0]
        type_map = {
            "definition": QuestionType.DEFINITION,
            "example": QuestionType.EXAMPLE,
            "how_to": QuestionType.HOW_TO,
            "comparison": QuestionType.COMPARISON,
            "troubleshooting": QuestionType.TROUBLESHOOTING
        }
        return type_map.get(best_type, QuestionType.GENERAL)
    
    def _calculate_confidence(self, match: Dict, q_type: QuestionType, text: str) -> float:
        score = 0.5
        
        # Clear question type boosts confidence
        if q_type != QuestionType.GENERAL:
            score += 0.2
        
        # Longer, complete questions boost confidence
        word_count = len(text.split())
        if word_count >= 3:
            score += 0.15
        if word_count >= 6:
            score += 0.1
        
        # Question marks indicate questions
        if "?" in text:
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_response(self, conv_matches: List[Match], intent: Intent, original_input: str) -> Tuple[str, Optional[str]]:
        has_conversation = len(conv_matches) > 0
        has_learning = intent.confidence >= 0.4 and intent.topic
        
        # Always prioritise learning over help requests
        if has_learning:
            if intent.topic.startswith("multiple:"):
                return self._handle_multiple_topics(intent), intent.topic
            else:
                response = self._generate_learning_response(intent)
                
                # Add brief greeting if present
                if has_conversation and conv_matches[0].priority == 1:
                    greeting = conv_matches[0].response.split('!')[0] + '!'
                    response = greeting + " " + response
                return response, intent.topic
        
        # Only handle pure conversational intents if no learning detected
        if has_conversation:
            return conv_matches[0].response, None
        
        # Fallback
        return "I'm not sure I understand. Try asking about JavaScript concepts like variables, functions, or arrays!", None

    def _handle_multiple_topics(self, intent: Intent) -> str:
        topics = intent.topic.replace("multiple:", "").split(',')
        return f"I think you are asking about multiple topics: {', '.join(topics)}. Could you clarify which one you want first?"

    def _generate_learning_response(self, intent: Intent) -> str:
        if intent.question_type == QuestionType.EXAMPLE:
            # Directly return the example
            example = get_example(intent.topic)
            return example

        base_info = self.js_facts.get(intent.topic, f"I don't have information on {intent.topic} yet.")

        type_responses = {
            QuestionType.DEFINITION: f"{base_info}\n\nWould you like to see an example?",
            QuestionType.HOW_TO: f"{base_info}\n\nWant me to explain any part in more detail?",
            QuestionType.COMPARISON: f"{base_info}\n\nWhat specifically did you want to compare it with?",
            QuestionType.TROUBLESHOOTING: f"{base_info}\n\nWhat specific problem are you having? Can you share your code?"
        }

        return type_responses.get(intent.question_type, f"{base_info}\n\nWhat else would you like to know about {intent.topic}?")

    def _map_keyword_to_topic(self, keyword: str) -> Optional[str]:
        for topic, synonyms in self.synonyms.items():
            if keyword in synonyms:
                return topic
        return None

    # Semantic search for paraphrased inputs
    def semantic_search_topic(self, user_input: str) -> Optional[str]:
        user_emb = self.model.encode(user_input)
        best_topic = None
        best_score = 0.0
        for topic, emb in self.fact_embeddings.items():
            sim = util.cos_sim(user_emb, emb)
            if sim > best_score and sim > 0.6:
                best_score = sim
                best_topic = topic
        return best_topic