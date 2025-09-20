from data import js_facts
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
        
        # Topic synonyms for keyword matching
        self.topic_synonyms = {
            "function": ["function", "functions", "method", "methods", "func"],
            "variable": ["variable", "variables", "var", "let", "const", "declaration"],
            "array": ["array", "arrays", "list", "lists"],
            "object": ["object", "objects", "obj", "dictionary"],
            "loop": ["loop", "loops", "iteration", "iterate", "for", "while", "for loop", "while loop"],
            "conditional": ["if", "else", "switch", "condition", "conditional", "if statement"],
            "event": ["event", "events", "listener", "click", "submit"],
            "string": ["string", "strings", "text"],
            "number": ["number", "numbers", "numeric"],
            "boolean": ["boolean", "booleans", "true", "false"],
            "dom": ["dom", "document", "html", "element"],
            "async": ["async", "await", "promise", "promises", "asynchronous"],
            "json": ["json", "parse", "stringify"],
            "console": ["console", "log", "debug", "debugging"],
        }
        
        # Question type patterns
        self.question_patterns = {
            QuestionType.DEFINITION: [
                r"what (is|are)",
                r"define",
                r"definition of",
                r"meaning of",
                r"explain",
                r"tell me about"
            ],
            QuestionType.EXAMPLE: [
                r"example",
                r"show me",
                r"demonstrate",
                r"sample",
                r"can you show"
            ],
            QuestionType.HOW_TO: [
                r"how (do|to)",
                r"how can i",
                r"steps to",
                r"process of"
            ],
            QuestionType.COMPARISON: [
                r"difference between",
                r"compare",
                r"vs",
                r"versus",
                r"better"
            ],
            QuestionType.TROUBLESHOOTING: [
                r"error",
                r"not working",
                r"problem",
                r"issue",
                r"fix",
                r"debug"
            ]
        }

    def get_response(self, user_input: str) -> str:
        original_input = user_input
        user_input = user_input.lower()
        self.memory.store_turn("user", user_input)

        # check for follow-up yes/no
        last_bot = self.memory.get_last_bot_turn()
        last_topic = self.memory.get_last_topic()
        if last_bot and last_topic and "Want me to explain more?" in last_bot["text"]:
            if user_input in ["yes", "y"]:
                response = js_facts.get(last_topic, f"Sorry, I have no info on {last_topic}.")
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

        # Enhanced intent extraction
        intent = self.extract_intent(original_input)
        
        # If we have high confidence, use the enhanced response
        if intent.confidence >= 0.4 and intent.topic:
            response = self.generate_enhanced_response(intent)
            self.memory.store_turn("bot", response, topic=intent.topic)
            return response

        # Use your original keyword matching for backward compatibility
        matches = [(keyword, fact) for keyword, fact in js_facts.items() if keyword.lower() in user_input.lower()]
        if matches:
            keyword, fact = matches[0]
            # Try to determine question type for this match
            question_type = self._determine_question_type(original_input)
            response = self._customize_response_by_type(fact, keyword, question_type)
            self.memory.store_turn("bot", response, topic=keyword)
            return response

        # Fallback generic response
        last_turns = [h for h in self.memory.get_history() if h["speaker"] == "user"]
        last_meaningful = None
        last_matched_keyword = None  # track the keyword that was matched
        
        for turn in reversed(last_turns[:-1]):  # skip the last turn
            text = turn["text"].lower()
            if text not in CONFUSED_INPUTS and text not in ["yes", "no", "y", "n"]:
                last_meaningful = turn["text"]
                # find which keyword was matched in that turn
                for keyword in js_facts.keys():
                    if keyword.lower() in text:
                        last_matched_keyword = keyword
                        break
                break

        if last_meaningful and last_matched_keyword:
            response = f"I'm not sure about that. Earlier you asked me about '{last_meaningful}'. Want me to explain more?"
            # store the matched keyword, not the full question
            self.memory.store_turn("bot", response, topic=last_matched_keyword)
        else:
            response = self._handle_no_matches(original_input)
            self.memory.store_turn("bot", response)

        return response

    def extract_intent(self, user_input: str) -> Intent:
        # Extract topic and question type from user input
        user_input_lower = user_input.lower()
        
        # Find matching topics using synonyms
        found_topics = []
        found_keywords = []
        
        # Check synonyms first
        for topic, synonyms in self.topic_synonyms.items():
            for synonym in synonyms:
                if synonym in user_input_lower:
                    found_topics.append(topic)
                    found_keywords.append(synonym)
                    break
        
        # Also check your original js_facts keys
        for keyword in js_facts.keys():
            if keyword.lower() in user_input_lower:
                if keyword not in found_keywords:
                    found_keywords.append(keyword)
                # Try to map to a topic
                mapped_topic = self._map_keyword_to_topic(keyword)
                if mapped_topic and mapped_topic not in found_topics:
                    found_topics.append(mapped_topic)
        
        # Determine question type
        question_type = self._determine_question_type(user_input)
        
        # Resolve primary topic if multiple found
        primary_topic = self._resolve_primary_topic(found_topics, user_input_lower)
        
        # Calculate confidence
        confidence = self._calculate_confidence(found_keywords, question_type, user_input)
        
        return Intent(
            topic=primary_topic,
            question_type=question_type,
            confidence=confidence,
            keywords_found=found_keywords
        )

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
        
        for q_type, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    return q_type
        
        return QuestionType.GENERAL

    def _resolve_primary_topic(self, topics: List[str], user_input: str) -> Optional[str]:
        # Choose the most relevant topic when multiple are found
        if not topics:
            return None
        if len(topics) == 1:
            return topics[0]
        
        # Use memory context if available
        last_topic = self.memory.get_last_topic()
        if last_topic and last_topic in topics:
            return last_topic
        
        # Score by position in sentence
        topic_scores = {}
        for topic in topics:
            score = 0
            for synonym in self.topic_synonyms.get(topic, [topic]):
                if synonym in user_input:
                    position = user_input.find(synonym)
                    score += (len(user_input) - position) / len(user_input)
            topic_scores[topic] = score
        
        return max(topic_scores, key=topic_scores.get) if topic_scores else topics[0]

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
        if topic in js_facts:
            return js_facts[topic]
        
        # Try to find related entries
        for key, value in js_facts.items():
            if topic in key.lower() or key.lower() in topic:
                return value
        
        # Try synonyms
        if topic in self.topic_synonyms:
            for synonym in self.topic_synonyms[topic]:
                if synonym in js_facts:
                    return js_facts[synonym]
                # Check if synonym is part of any key
                for key, value in js_facts.items():
                    if synonym in key.lower():
                        return value
        
        return f"I don't have specific information about {topic}."

    def _customize_response_by_type(self, base_info: str, topic: str, question_type: QuestionType) -> str:
        # Customise response based on question type
        if question_type == QuestionType.DEFINITION:
            return f"{base_info}\n\nWould you like to see an example?"
        
        elif question_type == QuestionType.EXAMPLE:
            return f"Here's about {topic}:\n\n{base_info}\n\nNeed help with a specific use case?"
        
        elif question_type == QuestionType.HOW_TO:
            return f"Here's how to work with {topic}:\n\n{base_info}\n\nWant me to explain any part in more detail?"
        
        elif question_type == QuestionType.COMPARISON:
            return f"About {topic}:\n\n{base_info}\n\nWhat specifically did you want to compare it with?"
        
        elif question_type == QuestionType.TROUBLESHOOTING:
            return f"Here's info about {topic}:\n\n{base_info}\n\nWhat specific problem are you having?"
        
        else:
            return f"{base_info}\n\nWhat else would you like to know about {topic}?"

    def _handle_no_matches(self, user_input: str) -> str:
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
