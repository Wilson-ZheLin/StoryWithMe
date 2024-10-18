import json
import os
import uuid

class Story:

    def __init__(self, content: str):
        self.uuid = str(uuid.uuid4())
        self.content = content
        self.parts = [part.strip() for part in self.content.split("\\") if part.strip()]
        self.illustration_links = []
        self.voice_links = []
        self.pages = len(self.parts)
        self.cursor = -1
        self.title = ""
    
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
    
    def get_current_page(self) -> str:
        if 0 <= self.cursor < self.pages:
            return self.parts[self.cursor]
    
    # For interaction with AI
    def get_current_progress_parts(self) -> str:
        return ' '.join(self.parts[:self.cursor + 1])
    
    def recreate_story(self, new_story_content: str):
        self.parts = self.parts[:self.cursor + 1] + [part.strip() for part in new_story_content.split("\\") if part.strip()]
        self.content = '\n \\ \n'.join(self.parts)
        self.illustration_links = self.illustration_links[:self.cursor + 1]
        self.voice_links = self.voice_links[:self.cursor + 1]
        self.pages = len(self.parts)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "content": self.content,
            "parts": self.parts,
            "illustration_links": self.illustration_links,
            "voice_links": self.voice_links,
            "pages": self.pages,
            "cursor": self.cursor,
            "title": self.title
        }

    def save_as_json(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # server dir
        story_dir = os.path.join(base_dir, "static", "story") # story dir
        if not os.path.exists(story_dir):
            os.makedirs(story_dir)
        path = os.path.join(story_dir, f"{self.uuid}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)