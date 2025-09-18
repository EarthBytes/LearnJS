from data import js_facts
from memory import Memory

class Chatbot:
    def __init__(self):
        self.memory = Memory()

    def get_response(self, user_input: str) -> str:
        self.memory.store_turn("user", user_input)

        # Check JS data for answers
        for keyword, fact in js_facts.items():
            if keyword.lower() in user_input.lower():
                response = fact
                self.memory.store_turn("bot", response)
                return response
        
        # Fallback generic response
        response = "I'm not sure about that. Can you ask something else about JavaScript?"
        self.memory.store_turn("bot", response)
        return response
