class Conversation:

    def __init__(self):
        self.dialogue = []
    
    def add_message(self, sender: str, message: str):
        if sender not in ['assistant', 'user']:
            raise ValueError('Invalid sender to format the conversation history!')
        self.dialogue.append({'role': sender, 'content': message})
    
    def get_conversation(self) -> list[dict]:
        return self.dialogue