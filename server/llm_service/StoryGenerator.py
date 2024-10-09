import logging
import os
import yaml
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class StoryGenerator:

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s  %(message)s')

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.model_name = self.config["model_name"]
        self.api_key = self.config["openai_api_key"]

    def generate_story(self, age: int, read_time: int, elements: list[str]):
        llm = ChatOpenAI(model_name=self.model_name, openai_api_key=self.api_key, temperature=1.0, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
        template = self.config["story_template"]
        prompt_template = PromptTemplate(
            input_variables=["age", "read_time", "elements"],
            template=template
        )
        summary_prompt = prompt_template.format(age=age, read_time=read_time, elements=', '.join(elements))
        logging.info("\nThe message sent to LLMs:\n" + summary_prompt)
        logging.info("\n" + "=" * 30 + "LLM Response: " + "=" * 30 + "\n")
        gpt_answer = llm([HumanMessage(content=summary_prompt)])
        return gpt_answer.content

# Example usage
if __name__ == "__main__":
    content_processor = StoryGenerator()
    llm_response = content_processor.generate_story(age=5, read_time=1, elements=["sci-fi", "space", "time travel"])