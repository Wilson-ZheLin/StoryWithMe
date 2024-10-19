import json
import os
import uuid

class Story:

    def __init__(self, content: str):
        self.uuid = str(uuid.uuid4())
        self.content = content
        self.parts = [part.strip() for part in self.content.split("||") if part.strip()]
        self.pages = len(self.parts)
        self.illustration_links = {i: "" for i in range(self.pages)}
        self.voice_links = {i: "" for i in range(self.pages)}
        self.cursor = -1
        self.title = ""
        self.narrator = "Rachel"
    
    def next_page(self) -> str:
        if self.cursor >= self.pages - 1:
            return None
        self.cursor += 1
        self.save_as_json()
        return self.parts[self.cursor]
    
    def previous_page(self) -> str:
        if self.cursor <= 0:
            return None
        self.cursor -= 1
        self.save_as_json()
        return self.parts[self.cursor]
    
    def get_current_page(self) -> str:
        if 0 <= self.cursor < self.pages:
            return self.parts[self.cursor]
    
    # For interaction with AI
    def get_current_progress_parts(self) -> str:
        return ' '.join(self.parts[:self.cursor + 1])
    
    def recreate_story(self, new_story_content: str):
        self.parts = self.parts[:self.cursor + 1] + [part.strip() for part in new_story_content.split("||") if part.strip()]
        self.content = '\n || \n'.join(self.parts)
        self.pages = len(self.parts)
        for i in range(self.cursor + 1, self.pages):
            self.illustration_links[i] = ""
            self.voice_links[i] = ""
        self.save_as_json()

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "content": self.content,
            "parts": self.parts,
            "illustration_links": self.illustration_links,
            "voice_links": self.voice_links,
            "pages": self.pages,
            "cursor": self.cursor,
            "title": self.title,
            "narrator": self.narrator
        }

    def save_as_json(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # server dir
        story_dir = os.path.join(base_dir, "static", "story") # story dir
        if not os.path.exists(story_dir):
            os.makedirs(story_dir)
        path = os.path.join(story_dir, f"{self.uuid}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_file_path(uuid: str):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # server dir
        story_dir = os.path.join(base_dir, "static", "story") # story folder dir
        return os.path.join(story_dir, f"{uuid}.json") # file dir

    @staticmethod
    def check_file_exists(uuid: str):
        return os.path.exists(Story.get_file_path(uuid))

    @classmethod
    def load_story_from_json(cls, uuid: str):
        if not Story.check_file_exists(uuid):
            raise FileNotFoundError(f"The file {uuid} does not exist.")

        with open(Story.get_file_path(uuid), 'r', encoding='utf-8') as file:
            data = json.load(file)
        story = cls(data['content'])
        story.__dict__.update(data)
        return story

if __name__ == "__main__":
    story = Story("Story Part 0 || Part 1 || Part 2 || Part 3 || Part 4")
    story.title = "This is a Title"
    story.save_as_json()