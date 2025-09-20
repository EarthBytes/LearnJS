class Memory:
    def __init__(self, max_turns: int = 5):
        self.history = []
        self.max_turns = max_turns
    
    def store_turn(self, speaker: str, text: str, topic: str = None):
        # Stores a turn
        self.history.append({"speaker": speaker, "text": text, "topic": topic})
        # keep memory short
        if len(self.history) > self.max_turns:  # use the correct attribute
            self.history.pop(0)

    def get_history(self):
        return self.history

    def get_last_bot_turn(self):
        # Return most recent bot turn or none
        for turn in reversed(self.history):
            if turn["speaker"] == "bot":
                return turn
        return None

    def get_last_topic(self):
        # Return the topic from the last bot turn if it exists
        last_bot = self.get_last_bot_turn()
        return last_bot.get("topic") if last_bot and "topic" in last_bot else None