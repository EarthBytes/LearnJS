from data import ( js_facts, conversation_prompts, user_status_responses, topic_synonyms, question_patterns )
from memory import Memory
import re
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
import difflib
from examples import get_example, get_all_examples_for_topic

CONFUSED_INPUTS = {"huh?", "what?", "?", "idk", "i don't understand", "explain", "can you repeat?", "confused"}
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
    keywords_found: List[str]

@dataclass
class ConversationalMatch:
    prompt: str
    response: str
    priority: int
    position: int
    length: int  # Length of the matched phrase

class EnhancedChatbot:
    def __init__(self):
        self.memory = Memory(max_turns=5)
        
        # Import all data from data.py
        self.js_facts = js_facts
        self.conversation_prompts = conversation_prompts
        self.user_status_responses = user_status_responses
        self.topic_synonyms = topic_synonyms
        self.question_patterns = question_patterns
        
        # Create normalized conversation prompts for better matching
        self._create_normalized_prompts()
        
    def _create_normalized_prompts(self):
        self.normalized_prompts = {}
        for prompt, data in self.conversation_prompts.items():
            # Remove punctuation and normalise
            normalized = self._normalize_text(prompt)
            self.normalized_prompts[normalized] = {
                'original': prompt,
                'data': data
            }

    def _normalize_text(self, text: str) -> str:
        # Remove common punctuation but keep letters, numbers and spaces
        normalized = re.sub(r"[^\w\s]", "", text.lower())
        # Replace multiple spaces with single space
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    def _is_nonsense_input(self, user_input: str) -> bool:
        # Determine if input is mostly nonsense
        words = user_input.lower().split()
        if len(words) == 0:
            return True
            
        meaningful_words = 0
        
        # Check against known keywords and conversation prompts
        for word in words:
            # Check if word is in any topic synonym
            for topic, synonyms in self.topic_synonyms.items():
                if any(word in synonym.lower() for synonym in synonyms):
                    meaningful_words += 1
                    break
            else:
                # Check if word is in conversation prompts
                if any(word in prompt.lower() for prompt in self.conversation_prompts.keys()):
                    meaningful_words += 1
                # Check common English words (basic list)
                elif word in {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'what', 'how', 'when', 'where', 'why', 'who', 'which', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}:
                    meaningful_words += 1
        
        ratio = meaningful_words / len(words)
        return ratio < NONSENSE_THRESHOLD

    def get_response(self, user_input: str) -> str:
        original_input = user_input
        user_input_lower = user_input.lower()
        self.memory.store_turn("user", user_input_lower)

        # Check for nonsense input
        if self._is_nonsense_input(user_input):
            response = "I'm not quite sure what you're asking about. Can you ask me something about JavaScript?\n\nI can help with: variables, functions, arrays, objects, loops, conditionals, DOM, events, and more!"
            self.memory.store_turn("bot", response)
            return response

        # Check for user status replies after bot asked "How are you?"
        if self._handle_status_response(user_input_lower):
            return self._handle_status_response(user_input_lower)

        # Handle follow-up yes/no responses
        follow_up_response = self._handle_follow_up_response(user_input_lower)
        if follow_up_response:
            return follow_up_response

        # Find all conversational matches 
        conversational_matches = self._find_enhanced_conversational_prompts(user_input_lower)
        
        # Extract learning intent
        learning_intent = self.extract_enhanced_intent(original_input)
        
        # Handle multiple intents with improved prioritisation
        response = self._handle_enhanced_multiple_intents(conversational_matches, learning_intent, original_input)
        
        # Store response with appropriate topic
        if learning_intent.topic and learning_intent.confidence >= 0.4:
            # Store just the topic name, not complex multi-topic strings
            topic_to_store = learning_intent.topic.split(':')[0] if ':' in learning_intent.topic else learning_intent.topic
            self.memory.store_turn("bot", response, topic=topic_to_store)
        else:
            self.memory.store_turn("bot", response)

        return response

    def _handle_status_response(self, user_input: str) -> Optional[str]:
        # Handle responses to 'how are you' questions
        last_bot = self.memory.get_last_bot_turn()
        if not last_bot:
            return None
            
        last_bot_text = last_bot["text"].lower()
        
        if any(phrase in last_bot_text for phrase in ["how are you", "how's it going", "how are you doing"]):
            for status, data in self.user_status_responses.items():
                if status in user_input:
                    response = data["response"]
                    self.memory.store_turn("bot", response)
                    return response
        return None

    def _handle_follow_up_response(self, user_input: str) -> Optional[str]:
        # check for follow-up yes/no
        last_bot = self.memory.get_last_bot_turn()
        last_topic = self.memory.get_last_topic()
        
        if last_bot and last_topic and ("Would you like to see an example?" in last_bot["text"] or "Want me to explain more?" in last_bot["text"]):
            if user_input in ["yes", "y"]:
                # Get detailed example from examples system
                detailed_response = self._get_detailed_topic_info(last_topic)
                self.memory.store_turn("bot", detailed_response)
                return detailed_response
            elif user_input in ["no", "n"]:
                response = "No problem! You can ask about another topic."
                self.memory.store_turn("bot", response)
                return response
            else:
                response = "I didn't quite get that. Please reply 'yes' or 'no'."
                self.memory.store_turn("bot", response)
                return response
        return None

    def _get_detailed_topic_info(self, topic: str) -> str:
        # Get more detailed information about a topic
        example = get_example(topic)
        if "I don't have specific examples" not in example:
            return example

        # Fall back to basic info with additional context
        basic_info = self._get_topic_info(topic)
        return f"{basic_info}\n\nHere's what you can try:\n• Ask for specific examples\n• Request step-by-step explanations\n• Ask about common use cases"

    def _find_enhanced_conversational_prompts(self, user_input: str) -> List[ConversationalMatch]:
        matches = []
        normalized_input = self._normalize_text(user_input)
        
        # Direct matching with original algorithm
        for prompt, data in self.conversation_prompts.items():
            if prompt in user_input:
                position = user_input.find(prompt)
                matches.append(ConversationalMatch(
                    prompt=prompt,
                    response=data['response'],
                    priority=data['priority'],
                    position=position,
                    length=len(prompt)
                ))
        
        # Matching with normalised text
        for normalized_prompt, prompt_data in self.normalized_prompts.items():
            if normalized_prompt in normalized_input:
                original_prompt = prompt_data['original']
                # Avoid duplicates
                if not any(m.prompt == original_prompt for m in matches):
                    position = normalized_input.find(normalized_prompt)
                    matches.append(ConversationalMatch(
                        prompt=original_prompt,
                        response=prompt_data['data']['response'],
                        priority=prompt_data['data']['priority'],
                        position=position,
                        length=len(normalized_prompt)
                    ))
        
        # Sort by priority (higher first), then by length (longer first), then by position (earlier first)
        return sorted(matches, key=lambda x: (-x.priority, -x.length, x.position))

    def extract_enhanced_intent(self, user_input: str) -> Intent:
        user_input_lower = user_input.lower()
        
        # Find all topic matches with positions and confidence scores
        topic_matches = []
        
        # Check synonyms first
        for topic, synonyms in self.topic_synonyms.items():
            for synonym in synonyms:
                # Exact match
                if synonym in user_input_lower:
                    position = user_input_lower.find(synonym)
                    topic_matches.append({
                        'topic': topic,
                        'keyword': synonym,
                        'position': position,
                        'length': len(synonym),
                        'confidence': 1.0,
                        'match_type': 'exact'
                    })
                else:
                    # Fuzzy match for typos (only for longer words)
                    if len(synonym) >= 4:
                        words_in_input = user_input_lower.split()
                        for word in words_in_input:
                            if len(word) >= 4:
                                similarity = difflib.SequenceMatcher(None, synonym, word).ratio()
                                if similarity >= 0.8:
                                    position = user_input_lower.find(word)
                                    topic_matches.append({
                                        'topic': topic,
                                        'keyword': word,
                                        'position': position,
                                        'length': len(word),
                                        'confidence': similarity,
                                        'match_type': 'fuzzy'
                                    })
        
        # Also check your original js_facts keys
        for keyword in self.js_facts.keys():
            if keyword.lower() in user_input_lower:
                position = user_input_lower.find(keyword.lower())
                mapped_topic = self._map_keyword_to_topic(keyword)
                # Avoid duplicates
                if not any(match['topic'] == (mapped_topic or keyword) and match['match_type'] == 'exact' for match in topic_matches):
                    topic_matches.append({
                        'topic': mapped_topic or keyword,
                        'keyword': keyword,
                        'position': position,
                        'length': len(keyword),
                        'confidence': 1.0,
                        'match_type': 'exact'
                    })
        
        # Remove duplicates and sort by confidence, then position
        seen_topics = set()
        unique_matches = []
        for match in sorted(topic_matches, key=lambda x: (-x['confidence'], x['position'])):
            topic_key = f"{match['topic']}_{match['position']}"
            if topic_key not in seen_topics:
                unique_matches.append(match)
                seen_topics.add(topic_key)
        
        # Group by topic to avoid multiple mentions of same topic
        topic_groups = defaultdict(list)
        for match in unique_matches:
            topic_groups[match['topic']].append(match)
        
        # Take best match per topic
        final_matches = []
        for topic, matches in topic_groups.items():
            best_match = max(matches, key=lambda x: x['confidence'])
            final_matches.append(best_match)
        
        # Sort by position for final ordering
        final_matches.sort(key=lambda x: x['position'])
        
        # Determine question type
        question_type = self._determine_enhanced_question_type(user_input)
        
        # Create intent based on matches
        if len(final_matches) > 1:
            # Multiple topics
            topics = [match['topic'] for match in final_matches]
            keywords = [match['keyword'] for match in final_matches]
            primary_topic = f"multiple:{','.join(topics)}"
            # Calculate confidence based on matches
            confidence = min(0.9, sum(match['confidence'] for match in final_matches) / len(final_matches))
            
            return Intent(
                topic=primary_topic,
                question_type=question_type,
                confidence=confidence,
                keywords_found=keywords
            )
        elif len(final_matches) == 1:
            # Single topic
            match = final_matches[0]
            confidence = self._calculate_enhanced_confidence([match['keyword']], question_type, user_input, match['confidence'])
            
            return Intent(
                topic=match['topic'],
                question_type=question_type,
                confidence=confidence,
                keywords_found=[match['keyword']]
            )
        else:
            # No topics found
            confidence = self._calculate_enhanced_confidence([], question_type, user_input, 0.0)
            return Intent(
                topic=None,
                question_type=question_type,
                confidence=confidence,
                keywords_found=[]
            )

    def _determine_enhanced_question_type(self, user_input: str) -> QuestionType:
        # Question type determines pattern matching
        user_input_lower = user_input.lower()
        
        # Score each question type
        type_scores = defaultdict(int)
        
        for q_type_str, patterns in self.question_patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, user_input_lower))
                if matches > 0:
                    type_scores[q_type_str] += matches
        
        # Special handling for troubleshooting
        troubleshooting_keywords = ['error', 'issue', 'problem', 'not working', 'fix', 'debug', 'broken', 'wrong']
        for keyword in troubleshooting_keywords:
            if keyword in user_input_lower:
                type_scores['troubleshooting'] += 2  # Higher weight for troubleshooting
        
        # Return the highest scoring type
        if type_scores:
            best_type = max(type_scores.items(), key=lambda x: x[1])[0]
            type_mapping = {
                "definition": QuestionType.DEFINITION,
                "example": QuestionType.EXAMPLE,
                "how_to": QuestionType.HOW_TO,
                "comparison": QuestionType.COMPARISON,
                "troubleshooting": QuestionType.TROUBLESHOOTING
            }
            return type_mapping.get(best_type, QuestionType.GENERAL)
        
        return QuestionType.GENERAL

    def _calculate_enhanced_confidence(self, keywords: List[str], question_type: QuestionType, user_input: str, base_match_confidence: float) -> float:
        base_score = 0.1
        
        # Keyword matches boost confidence
        if keywords:
            keyword_score = 0.5 * min(len(keywords) / 2, 1.0)
            # Factor in match quality (for fuzzy matches)
            keyword_score *= max(base_match_confidence, 0.7)
            base_score += keyword_score
        
        # Clear question type boosts confidence
        if question_type != QuestionType.GENERAL:
            base_score += 0.2
        
        # Longer, complete questions boost confidence
        word_count = len(user_input.split())
        if word_count >= 3:
            base_score += 0.15
        if word_count >= 6:
            base_score += 0.1
        
        # Question marks indicate questions
        if "?" in user_input:
            base_score += 0.1
        
        return min(base_score, 1.0)

    def _handle_enhanced_multiple_intents(self, conversational_matches: List[ConversationalMatch], learning_intent: Intent, original_input: str) -> str:
        
        has_conversation = len(conversational_matches) > 0
        has_learning = learning_intent.confidence >= 0.4 and learning_intent.topic
        
        # Always prioritize learning over help requests
        if has_learning:
            # If there's any learning intent, handle it first and ignore help requests
            if learning_intent.topic and learning_intent.topic.startswith("multiple:"):
                return self._handle_multiple_topics(learning_intent)
            else:
                response = self.generate_enhanced_response(learning_intent)
                # Only add conversational elements if they're greetings (priority 1)
                if has_conversation and conversational_matches[0].priority == 1:
                    brief_greeting = conversational_matches[0].response.split('!')[0] + "!"
                    return f"{brief_greeting} {response}"
                return response
        
        # Only handle pure conversational intents if no learning detected
        elif has_conversation:
            return conversational_matches[0].response
        
        else:
            return self._handle_enhanced_fallback(original_input)

    def _handle_multiple_topics(self, intent: Intent) -> str:
        # Handle multiple topics in a single intent
        topics_str = intent.topic.replace("multiple:", "")
        topics = topics_str.split(",")
        
        if len(topics) == 2:
            # Handle two topics
            topic1, topic2 = topics
            info1 = self._get_topic_info(topic1)
            info2 = self._get_topic_info(topic2)
            
            if intent.question_type == QuestionType.COMPARISON:
                return f"**{topic1.title()}:** {info1}\n\n**{topic2.title()}:** {info2}\n\nWhat specific aspects would you like me to compare?"
            else:
                return f"**{topic1.title()}:** {info1}\n\n**{topic2.title()}:** {info2}\n\nWould you like me to go deeper into either topic?"
        
        elif len(topics) > 2:
            topic_list = ", ".join([t.title() for t in topics[:-1]]) + f", and {topics[-1].title()}"
            return f"You're asking about {topic_list}! That's quite a bit to cover.\n\nWhich topic would you like me to start with?"
        
        else:
            return self._get_topic_info(topics[0])

    def _handle_enhanced_fallback(self, original_input: str) -> str:
        # Fallback handling
        user_input = original_input.lower()
        
        # Check for partial keyword matches with fuzzy matching
        matches = []
        for keyword, fact in self.js_facts.items():
            if keyword.lower() in user_input:
                matches.append((keyword, fact))
        
        # If no direct matches, try fuzzy matching
        if not matches:
            words_in_input = user_input.split()
            for word in words_in_input:
                if len(word) >= 4:  # Only try fuzzy matching for longer words
                    for keyword in self.js_facts.keys():
                        if len(keyword) >= 4:
                            similarity = difflib.SequenceMatcher(None, word, keyword.lower()).ratio()
                            if similarity >= 0.75:  # Low threshold for matching
                                matches.append((keyword, self.js_facts[keyword]))
                                break
        
        if matches:
            keyword, fact = matches[0]
            question_type = self._determine_enhanced_question_type(original_input)
            return self._customize_response_by_type(fact, keyword, question_type)

        # Memory-based fallback
        last_turns = [h for h in self.memory.get_history() if h["speaker"] == "user"]
        last_meaningful = None
        last_matched_keyword = None
        
        for turn in reversed(last_turns[:-1]):
            text = turn["text"].lower()
            if text not in CONFUSED_INPUTS and text not in ["yes", "no", "y", "n"]:
                last_meaningful = turn["text"]
                # Look for any topic in the last meaningful turn
                for topic, synonyms in self.topic_synonyms.items():
                    for synonym in synonyms:
                        if synonym in text:
                            last_matched_keyword = topic
                            break
                    if last_matched_keyword:
                        break
                break

        if last_meaningful and last_matched_keyword:
            return f"I'm not sure about that. Earlier you were asking about {last_matched_keyword}. Want me to explain more about that topic?"
        else:
            return self._handle_no_matches(original_input)

    def _map_keyword_to_topic(self, keyword: str) -> Optional[str]:
        # Map js_facts keyword to topic category
        keyword_lower = keyword.lower()
        
        # Map specific keywords to topics
        mappings = {
            "var": "variable", "let": "variable", "const": "variable",
            "for loop": "loop", "while loop": "loop", "for": "loop", "while": "loop",
            "if statement": "conditional", "if": "conditional", "else": "conditional",
            "arrays": "array", "objects": "object", "functions": "function",
            "strings": "string", "numbers": "number", "booleans": "boolean",
            "what is javascript": "javascript", "javascript basics": "basics"
        }
        
        # Check direct mapping
        if keyword_lower in mappings:
            return mappings[keyword_lower]
        
        # Check if keyword contains topic name
        for topic in self.topic_synonyms.keys():
            if topic in keyword_lower or keyword_lower in topic:
                return topic
        
        return keyword_lower

    def generate_enhanced_response(self, intent: Intent) -> str:
        # Generate response using intent understanding
        topic_info = self._get_topic_info(intent.topic)
        return self._customize_response_by_type(topic_info, intent.topic, intent.question_type)

    def _get_topic_info(self, topic: str) -> str:
        # Direct match
        if topic in self.js_facts:
            return self.js_facts[topic]
        
        # Check for related entries
        for key, value in self.js_facts.items():
            if topic.lower() in key.lower() or key.lower() in topic.lower():
                return value
        
        # Check synonyms
        if topic in self.topic_synonyms:
            for synonym in self.topic_synonyms[topic]:
                if synonym in self.js_facts:
                    return self.js_facts[synonym]
                for key, value in self.js_facts.items():
                    if synonym.lower() in key.lower():
                        return value
        
        return f"I don't have specific information about {topic}. Can you ask about something else in JavaScript?"

    def _customize_response_by_type(self, base_info: str, topic: str, question_type: QuestionType) -> str:
        # Customise response based on question type
        if question_type == QuestionType.DEFINITION:
            return f"{base_info}\n\nWould you like to see an example?"
        
        elif question_type == QuestionType.EXAMPLE:
            return f"{base_info}\n\nNeed help with a specific use case?"
        
        elif question_type == QuestionType.HOW_TO:
            return f"{base_info}\n\nWant me to explain any part in more detail?"
        
        elif question_type == QuestionType.COMPARISON:
            return f"{base_info}\n\nWhat specifically did you want to compare it with?"
        
        elif question_type == QuestionType.TROUBLESHOOTING:
            return f"{base_info}\n\nWhat specific problem are you having? Can you share your code?"
        
        else:
            return f"{base_info}\n\nWhat else would you like to know about {topic}?"

    def _handle_no_matches(self, user_input: str) -> str:
        # Handle no matches found
        # Try to suggest topics based on partial matches
        suggestions = self._get_enhanced_topic_suggestions(user_input)
        
        if suggestions:
            suggestions_text = ", ".join(suggestions)
            return f"I'm not sure about that. Are you asking about: {suggestions_text}?\n\nOr try asking something like:\n• 'What is a function?'\n• 'Show me an array example'\n• 'How do I use loops?'"
        
        return "I'm not quite sure what you're asking about. Can you ask me something about JavaScript?\n\nI can help with: variables, functions, arrays, objects, loops, conditionals, DOM, events, and more!"

    def _get_enhanced_topic_suggestions(self, user_input: str) -> List[str]:
        # Suggest topics with fuzzy matching
        suggestions = []
        user_words = user_input.lower().split()
        
        # Exact and partial matches
        for topic, synonyms in self.topic_synonyms.items():
            for word in user_words:
                if len(word) >= 3:
                    for synonym in synonyms:
                        # Exact match
                        if word == synonym or word in synonym or synonym in word:
                            if topic not in suggestions:
                                suggestions.append(topic)
                            break
                        # Fuzzy match for longer words
                        elif len(word) >= 4 and len(synonym) >= 4:
                            similarity = difflib.SequenceMatcher(None, word, synonym).ratio()
                            if similarity >= 0.7:
                                if topic not in suggestions:
                                    suggestions.append(topic)
                                break
        
        return suggestions[:3]

    def show_history(self):
        # Show conversation history#
        return self.memory.get_history()


# Alias for backward compatibility
Chatbot = EnhancedChatbot