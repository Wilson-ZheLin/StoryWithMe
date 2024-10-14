import os
import yaml
from langchain.prompts import PromptTemplate
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

class StoryGeneratorViaPortKey:

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.model_name = self.config["model_name"]
        self.api_key = self.config["openai_api_key"]
        self.portkey_api_key = self.config["portkey_api_key"]

    def generate(self, age: int, read_time: int, elements: list[str]):
        client = OpenAI(
            api_key=self.api_key,
            base_url=PORTKEY_GATEWAY_URL,
            default_headers=createHeaders(provider="openai", api_key=self.portkey_api_key)
        )
        prompt_system = PromptTemplate(input_variables=["age"], template=self.config["story_template_system"]).format(age=age)
        prompt_user = PromptTemplate(input_variables=["read_time", "elements"], template=self.config["story_template_user"]).format(read_time=read_time, elements=', '.join(elements))
        chat_complete = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ],
            stream=True
        )
        for chunk in chat_complete:
            yield chunk.choices[0].delta.content

if __name__ == '__main__':
    story_generator = StoryGeneratorViaPortKey()
    for content in story_generator.generate(age=5, read_time=1, elements=["sci-fi", "space", "time travel"]):
        if content is not None:
            print(content, end="", flush=True)