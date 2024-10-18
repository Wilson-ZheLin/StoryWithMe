import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from .StabilityService import StabilityService

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_service.LLMServiceViaPortKey import LLMServiceViaPortKey
from model.Story import Story

def generate_images_for_next_two_pages(story: Story):
    img_service = StabilityService()
    llm_service = LLMServiceViaPortKey()
    curr_page = story.cursor
    tasks = []

    # Concurrently generate images for next two pages
    with ThreadPoolExecutor() as executor:
        for i in range(curr_page + 1, curr_page + 3):
            if i >= story.pages: return
            if story.illustration_links[i]: continue
            
            def process_page(page_index):
                img_prompt = llm_service.generate_img_prompt(story.parts[page_index])
                img_service.generate_image(img_prompt, story.uuid + "_" + str(page_index))
                story.illustration_links[page_index] = story.uuid + "_" + str(page_index) + ".webp"

            tasks.append(executor.submit(process_page, i))

        for future in as_completed(tasks):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred while generating image: {e}")

    story.save_as_json()