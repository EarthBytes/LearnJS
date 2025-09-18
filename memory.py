class Memory:
    def __init__(self, max_turns: int = 5):
        self.history = []
        self.max_turns = max_turns  # fixed here
    
    def store_turn(self, speaker: str, text: str):
        self.history.append({"speaker": speaker, "text": text})
        # keep memory short
        if len(self.history) > self.max_turns:  # use the correct attribute
            self.history.pop(0)

    def get_history(self):
        return self.history
