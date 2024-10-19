from concurrent.futures import ThreadPoolExecutor, as_completed
from model.Story import Story
from img_service.StabilityService import StabilityService
from llm_service.LLMServiceViaPortKey import LLMServiceViaPortKey
from voiceover_service.tts_service import TTSService
from voiceover_service.voice_cloning_service import VoiceCloningService

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
    
def generate_voiceover_for_next_two_pages(story: Story, narrator: str = "Rachel"):
    tts_service = TTSService()
    curr_page = story.cursor
    input_arr = []
    index_map = []   
    
    for i in range(curr_page + 1, curr_page + 3):
        if i >= story.pages:
            return
        if story.voice_links[i]:  
            continue
        if story.parts[i]:  
            input_arr.append(story.parts[i])
            index_map.append(i)  
    
    audio_paths = tts_service.text_to_speech_save(
        session_texts=input_arr,
        voice=narrator
    )
    
    for idx, audio_path in enumerate(audio_paths):
        story.voice_links[index_map[idx]] = audio_path
        
    story.save_as_json()
