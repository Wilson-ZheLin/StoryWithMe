class Story:

    def __init__(self, content: str):
        self.content = content
        self.parts = [part.strip() for part in self.content.split("\\") if part.strip()]
        self.illustration_links = []
        self.pages = len(self.parts)
        self.cursor = -1
    
    def next_page(self) -> str:
        if self.cursor >= self.pages - 1:
            return None
        self.cursor += 1
        return self.parts[self.cursor]
    
    def previous_page(self) -> str:
        if self.cursor <= 0:
            return None
        self.cursor -= 1
        return self.parts[self.cursor]
    
    # For interaction with AI
    def get_current_progress_parts(self) -> str:
        return '\n'.join(self.parts[:self.cursor + 1])