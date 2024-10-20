import os
import yaml
from langchain.prompts import PromptTemplate
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

class LLMServiceViaPortKey:

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.model_name = self.config["model_name"]
        self.api_key = self.config["openai_api_key"]
        self.portkey_api_key = self.config["portkey_api_key"]
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=PORTKEY_GATEWAY_URL,
            default_headers=createHeaders(provider="openai", api_key=self.portkey_api_key)
        )

    def generate_story(self, age: int, read_time: int, elements: list[str], hobbies: list[str] = ["not specified"], mood: str = "not specified"):
        prompt_system = PromptTemplate(input_variables=["age"], template=self.config["story_template_system"]).format(age=age)
        prompt_user = PromptTemplate(input_variables=["read_time", "elements", "mood", "hobbies"], template=self.config["story_template_user"]).format(read_time=read_time, elements=', '.join(elements), mood=mood, hobbies=', '.join(hobbies))
        chat_complete = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ],
            stream=True
        )
        for chunk in chat_complete:
            yield chunk.choices[0].delta.content

    def recreate_story(self, story_so_far: str, read_time: int, new_elements: list[str]):
        prompt_system = PromptTemplate(input_variables=["story_so_far"], template=self.config["story_recreation_system"]).format(story_so_far=story_so_far)
        prompt_user = PromptTemplate(input_variables=["read_time", "new_elements"], template=self.config["story_recreation_user"]).format(read_time=read_time, new_elements=', '.join(new_elements))
        chat_complete = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ],
            stream=True
        )
        for chunk in chat_complete:
            yield chunk.choices[0].delta.content

    def interact(self, dialogue_history: list[dict], story: str):
        prompt_system = PromptTemplate(input_variables=["story"], template=self.config["interaction_system"]).format(story=story)
        chat_complete = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "system", "content": prompt_system}]+dialogue_history,
            stream=True
        )
        for chunk in chat_complete:
            yield chunk.choices[0].delta.content

    def generate_img_prompt(self, story_chunk: str, style: str = "Hayao Miyazaki"):
        prompt_user = PromptTemplate(input_variables=["story_chunk", "style"], template=self.config["image_prompt_template"]).format(story_chunk=story_chunk, style=style)
        chat_complete = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt_user}],
        )
        return chat_complete.choices[0].message.content

    def get_story_title(self, story: str):
        prompt_user = PromptTemplate(input_variables=["story"], template=self.config["story_title_template"]).format(story=story)
        chat_complete = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt_user}],
        )
        return chat_complete.choices[0].message.content
    
    def get_interaction_prompt(self, story_so_far: str):
        prompt_user = PromptTemplate(input_variables=["story_so_far"], template=self.config["interaction_prompt_template"]).format(story_so_far=story_so_far)
        chat_complete = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt_user}],
        )
        return chat_complete.choices[0].message.content

if __name__ == '__main__':
    llm_content_processor = LLMServiceViaPortKey()
    print("Test Generating Story: ")
    for content in llm_content_processor.generate_story(age=5, read_time=1, elements=["sci-fi", "space", "time travel"]):
        if content is not None:
            print(content, end="", flush=True)
