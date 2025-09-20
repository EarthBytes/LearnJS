from data import ( js_facts, conversation_prompts, user_status_responses, topic_synonyms, question_patterns )
from memory import Memory
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

CONFUSED_INPUTS = {"huh?", "what?", "?", "idk", "i don't understand", "explain", "can you repeat?", "confused"}

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

class Chatbot:
    def __init__(self):
        self.memory = Memory(max_turns=5)
        
        # Import all data from data.py
        self.js_facts = js_facts
        self.conversation_prompts = conversation_prompts
        self.topic_synonyms = topic_synonyms
        self.question_patterns = question_patterns

    def get_response(self, user_input: str) -> str:
        original_input = user_input
        user_input = user_input.lower()
        self.memory.store_turn("user", user_input)

        # Check for user status replies after bot asked "How are you?"

        if self.memory.get_last_bot_turn():
            last_bot_text = self.memory.get_last_bot_turn()["text"].lower()
            
            if any(phrase in last_bot_text for phrase in ["how are you", "how's it going", "how are you doing"]):
                for status, data in self.user_status_responses.items():
                    if status in user_input:
                        response = data["response"]
                        self.memory.store_turn("bot", response)
                        return response
                    
        # check for follow-up yes/no
        last_bot = self.memory.get_last_bot_turn()
        last_topic = self.memory.get_last_topic()
        if last_bot and last_topic and "Want me to explain more?" in last_bot["text"]:
            if user_input in ["yes", "y"]:
                response = self.js_facts.get(last_topic, f"Sorry, I have no info on {last_topic}.")
                self.memory.store_turn("bot", response)
                return response
            elif user_input in ["no", "n"]:
                response = "No problem! You can ask about another topic."
                self.memory.store_turn("bot", response)
                return response
            else:
                response = "I didn't quite get that. Please reply 'yes' or 'no'."
                self.memory.store_turn("bot", response)
                return response

        # Check for multiple intents (conversational + learning)
        conversational_matches = self._find_conversational_prompts(user_input)
        learning_intent = self.extract_intent(original_input)
        
        # Handle multiple intents with priority
        response = self._handle_multiple_intents(conversational_matches, learning_intent, original_input)
        
        # Store response with appropriate topic
        if learning_intent.topic and learning_intent.confidence >= 0.4:
            self.memory.store_turn("bot", response, topic=learning_intent.topic)
        else:
            self.memory.store_turn("bot", response)

        return response

    def extract_intent(self, user_input: str) -> Intent:
        # Extract topic and question type from user input
        user_input_lower = user_input.lower()
        
        # Find matching topics and their positions
        topic_matches = []
        
        # Check synonyms first
        for topic, synonyms in self.topic_synonyms.items():
            for synonym in synonyms:
                if synonym in user_input_lower:
                    position = user_input_lower.find(synonym)
                    topic_matches.append({
                        'topic': topic,
                        'keyword': synonym,
                        'position': position,
                        'length': len(synonym)
                    })
        
        # Also check your original js_facts keys
        for keyword in self.js_facts.keys():
            if keyword.lower() in user_input_lower:
                position = user_input_lower.find(keyword.lower())
                mapped_topic = self._map_keyword_to_topic(keyword)
                topic_matches.append({
                    'topic': mapped_topic or keyword,
                    'keyword': keyword,
                    'position': position,
                    'length': len(keyword)
                })
        
        # Remove duplicates and sort by position
        seen_topics = set()
        unique_matches = []
        for match in sorted(topic_matches, key=lambda x: x['position']):
            if match['topic'] not in seen_topics:
                unique_matches.append(match)
                seen_topics.add(match['topic'])
        
        # Determine question type
        question_type = self._determine_question_type(user_input)
        
        # If multiple topics, create combined response intent
        if len(unique_matches) > 1:
            # Create a multi-topic intent
            topics = [match['topic'] for match in unique_matches]
            keywords = [match['keyword'] for match in unique_matches]
            primary_topic = f"multiple:{','.join(topics)}"  # Special indicator for multiple topics
            confidence = 0.8  # High confidence since we found multiple clear topics
            
            return Intent(
                topic=primary_topic,
                question_type=question_type,
                confidence=confidence,
                keywords_found=keywords
            )
        
        # Single topic handling (existing logic)
        elif len(unique_matches) == 1:
            match = unique_matches[0]
            confidence = self._calculate_confidence([match['keyword']], question_type, user_input)
            
            return Intent(
                topic=match['topic'],
                question_type=question_type,
                confidence=confidence,
                keywords_found=[match['keyword']]
            )
        
        # No topics found
        else:
            confidence = self._calculate_confidence([], question_type, user_input)
            return Intent(
                topic=None,
                question_type=question_type,
                confidence=confidence,
                keywords_found=[]
            )

    def _find_conversational_prompts(self, user_input: str) -> List[Dict]:
        # Find conversational prompts in user input
        matches = []
        user_input_lower = user_input.lower()
        
        for prompt, data in self.conversation_prompts.items():
            if prompt in user_input_lower:
                position = user_input_lower.find(prompt)
                matches.append({
                    'prompt': prompt,
                    'response': data['response'],
                    'priority': data['priority'],
                    'position': position
                })
        
        # Sort by priority (higher first), then by position (earlier first)
        return sorted(matches, key=lambda x: (-x['priority'], x['position']))

    def _handle_multiple_intents(self, conversational_matches: List[Dict], learning_intent: Intent, original_input: str) -> str:
        # Determine if we have both conversational and learning intents
        
        has_conversation = len(conversational_matches) > 0
        has_learning = learning_intent.confidence >= 0.4 and learning_intent.topic
        
        # Case 1 - Both conversational and learning 
        if has_conversation and has_learning:
            # Get the highest priority conversational response
            conv_response = conversational_matches[0]['response']
            
            # Handle multiple topics in learning
            if learning_intent.topic and learning_intent.topic.startswith("multiple:"):
                learning_response = self._handle_multiple_topics(learning_intent)
            else:
                learning_response = self.generate_enhanced_response(learning_intent)
            
            # Combine responses based on priority
            if conversational_matches[0]['priority'] >= 3:  # High priority conversation
                return f"{conv_response}\n\n{learning_response}"
            else:  # Low/medium priority
                return f"{conv_response} {learning_response}"
        
        # Case 2 - Only conversational
        elif has_conversation and not has_learning:
            return conversational_matches[0]['response']
        
        # Case 3 - Only learning (multiple topics)
        elif has_learning and learning_intent.topic and learning_intent.topic.startswith("multiple:"):
            return self._handle_multiple_topics(learning_intent)
        
        # Case 4 - Only learning (single topic)
        elif has_learning:
            return self.generate_enhanced_response(learning_intent)
        
        # Case 5 - Fallback to original logic
        else:
            return self._handle_fallback_logic(original_input)

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
                return f"{topic1.title()} vs {topic2.title()}:\n\n{topic1.title()}:{info1}\n\n{topic2.title()}: {info2}\n\nWhich one would you like me to explain further?"
            else:
                return f"I can see you're asking about {topic1} and {topic2}!\n\n {info1}\n\n {info2}\n\nWhich topic interests you more?"
        
        elif len(topics) > 2:
            # Handle many topics
            topic_list = ", ".join([t.title() for t in topics[:-1]]) + f", and {topics[-1].title()}"
            return f"Wow, you're asking about {topic_list}! That's a lot to cover.\n\nWhich one would you like me to start with? Or would you prefer a brief overview of all of them?"
        
        else:
            # Shouldn't happen, but fallback
            return self._get_topic_info(topics[0])

    def _handle_fallback_logic(self, original_input: str) -> str:
        # Lowercase for matching but keep original for responses
        user_input = original_input.lower()
        
        # Check original keyword matching as fallback
        matches = [(keyword, fact) for keyword, fact in self.js_facts.items() if keyword.lower() in user_input]
        if matches:
            keyword, fact = matches[0]
            question_type = self._determine_question_type(original_input)
            return self._customize_response_by_type(fact, keyword, question_type)

        # Memory-based fallback
        last_turns = [h for h in self.memory.get_history() if h["speaker"] == "user"]
        last_meaningful = None
        last_matched_keyword = None
        
        for turn in reversed(last_turns[:-1]):
            text = turn["text"].lower()
            if text not in CONFUSED_INPUTS and text not in ["yes", "no", "y", "n"]:
                last_meaningful = turn["text"]
                for keyword in self.js_facts.keys():
                    if keyword.lower() in text:
                        last_matched_keyword = keyword
                        break
                break

        if last_meaningful and last_matched_keyword:
            return f"I'm not sure about that. Earlier you asked me about '{last_meaningful}'. Want me to explain more?"
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
            "strings": "string", "numbers": "number", "booleans": "boolean"
        }
        
        # Check direct mapping
        if keyword_lower in mappings:
            return mappings[keyword_lower]
        
        # Check if keyword contains topic name
        for topic in self.topic_synonyms.keys():
            if topic in keyword_lower or keyword_lower in topic:
                return topic
        
        return keyword_lower  # Return the keyword itself as topic

    def _determine_question_type(self, user_input: str) -> QuestionType:
        # determine what type of question is being asked
        user_input_lower = user_input.lower()
        
        for q_type_str, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    # Map string to enum
                    if q_type_str == "definition":
                        return QuestionType.DEFINITION
                    elif q_type_str == "example":
                        return QuestionType.EXAMPLE
                    elif q_type_str == "how_to":
                        return QuestionType.HOW_TO
                    elif q_type_str == "comparison":
                        return QuestionType.COMPARISON
                    elif q_type_str == "troubleshooting":
                        return QuestionType.TROUBLESHOOTING
        
        return QuestionType.GENERAL

    def _calculate_confidence(self, keywords: List[str], question_type: QuestionType, user_input: str) -> float:
        # Calculate confidence on intent
        base_score = 0.2
        
        # Keyword matches boost confidence
        if keywords:
            base_score += 0.4 * min(len(keywords) / 2, 1.0)
        
        # Clear question type boosts confidence
        if question_type != QuestionType.GENERAL:
            base_score += 0.2
        
        # Longer, complete questions boost confidence
        if len(user_input.split()) >= 3:
            base_score += 0.1
        
        # Question marks indicate questions
        if "?" in user_input:
            base_score += 0.1
        
        return min(base_score, 1.0)

    def generate_enhanced_response(self, intent: Intent) -> str:
        # Generate response using intent understanding
        topic_info = self._get_topic_info(intent.topic)
        return self._customize_response_by_type(topic_info, intent.topic, intent.question_type)

    def _get_topic_info(self, topic: str) -> str: # get information about a topic 
        # Try exact match in js_facts
        if topic in self.js_facts:
            return self.js_facts[topic]
        
        # Try to find related entries
        for key, value in self.js_facts.items():
            if topic in key.lower() or key.lower() in topic:
                return value
        
        # Try synonyms
        if topic in self.topic_synonyms:
            for synonym in self.topic_synonyms[topic]:
                if synonym in self.js_facts:
                    return self.js_facts[synonym]
                # Check if synonym is part of any key
                for key, value in self.js_facts.items():
                    if synonym in key.lower():
                        return value
        
        return f"I don't have specific information about {topic}."

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
            return f"{base_info}\n\nWhat specific problem are you having?"
        
        else:
            return f"{base_info}\n\nWhat else would you like to know about {topic}?"

    def _handle_no_matches(self, user_input: str) -> str:
        # Handle no matches found
        # Try to suggest topics based on partial matches
        suggestions = self._get_topic_suggestions(user_input)
        
        if suggestions:
            return f"I'm not sure about that. Are you asking about: {', '.join(suggestions)}?\n\nOr try asking something like:\n• 'What is a function?'\n• 'Show me an array example'\n• 'How do I use loops?'"
        
        return "I'm not sure about that. Can you ask something else about JavaScript?\n\nI can help with: variables, functions, arrays, objects, loops, conditionals, DOM, events, and more!"

    def _get_topic_suggestions(self, user_input: str) -> List[str]:
        # Suggest topics based on partial word matches
        suggestions = []
        user_words = user_input.lower().split()
        
        for topic, synonyms in self.topic_synonyms.items():
            for word in user_words:
                for synonym in synonyms:
                    if len(word) >= 3 and (word in synonym or synonym in word):
                        if topic not in suggestions:
                            suggestions.append(topic)
                        break
        
        return suggestions[:3]

    def show_history(self):
        return self.memory.get_history()


if __name__ == "__main__":
    bot = Chatbot()
    print("LearnJS (type 'quit' to exit)")

    while True:
        user_text = input("You: ")
        if user_text.lower() in ["quit", "exit", "bye"]:
            print("Bot: Goodbye!")
            break
        print("Bot:", bot.get_response(user_text))
