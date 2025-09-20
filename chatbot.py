from data import js_facts
from memory import Memory

CONFUSED_INPUTS = {"huh?", "what?", "?", "idk", "i don't understand", "explain", "can you repeat?", "confused"}

class Chatbot:
    def __init__(self):
        self.memory = Memory(max_turns=5)

    def get_response(self, user_input: str) -> str:
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

        # Check JS data for answers
        matches = [(keyword, fact) for keyword, fact in js_facts.items() if keyword.lower() in user_input.lower()]
        if matches:
            keyword, fact = matches[0]  # pick the first match
            response = fact
            # store the actual keyword as topic for follow-ups
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
            response = "I'm not sure about that. Can you ask something else about JavaScript?"
            self.memory.store_turn("bot", response)

        return response

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
