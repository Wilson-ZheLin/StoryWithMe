import os
from flask import Flask, jsonify, request, abort
from model.Conversation import Conversation
from model.Story import Story
from llm_service.voiceToText import voice_to_text
from llm_service.LLMServiceViaPortKey import LLMServiceViaPortKey
from util import generate_images_for_next_two_pages,generate_voiceover_for_next_two_pages,clone_user_voice

# from flask_cors import CORS
app = Flask(__name__)
# CORS(app)

# Store as global variables
app.config['dialogue'] = None
app.config['uuid'] = None

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/generate_story", methods=["POST"])
def generate_story():
    user_input = request.get_json()
    age = user_input["age"]
    read_time = user_input["readTime"]
    elements = user_input["elements"]
    mood = user_input["mood"]
    hobbies = user_input["hobbies"]
    voice_character = user_input["voiceCharacter"]
    voice_character_path = user_input["voiceCharacterPath"]
    llm_content_processor = LLMServiceViaPortKey()
    story_content = ''.join(chunk for chunk in llm_content_processor.generate_story(age, read_time, elements, hobbies, mood) if chunk is not None)
    story_obj = Story(story_content)
    app.config['uuid'] = story_obj.uuid
    story_obj.set_voice_character(voice_character, voice_character_path)
    story_obj.title = llm_content_processor.get_story_title(story_content)
    story_obj.question = llm_content_processor.get_interaction_prompt("\n".join(story_obj.parts[:3]))
    story_obj.save_as_json() # just to be safe
    generate_images_for_next_two_pages(story_obj)
    generate_voiceover_for_next_two_pages(story_obj) 
    return jsonify({'story': "\n\n".join(story_obj.parts)})

@app.route("/get_story", methods=["GET"])
def get_story():
    _check_story_created()
    return jsonify(_get_story_object().to_dict())

@app.route('/upload-parent', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400

    file = request.files['audio']
    
    if file.filename == '':
        jsonify({'status': 'error', 'message': 'File upload failed'}), 400

    if file:
        filename = file.filename
        sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"voiceover_service", "voice_samples", "parent.wav")
        file.save(sample_path)
        clone_user_voice(sample_path)
        return 'Audio cloned successfully', 200

@app.route('/upload-kid', methods=['POST'])
def upload_audio_for_kid():
    if 'audio' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400

    file = request.files['audio']
    
    if file.filename == '':
        jsonify({'status': 'error', 'message': 'File upload failed'}), 400

    if file:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"voiceover_service", "voice_samples", "kid.wav")
        file.save(file_path)
        voice_text = voice_to_text(file_path)
        llm_content_processor = LLMServiceViaPortKey()
        new_story_prompt = llm_content_processor.get_new_guideline(voice_text)
        if new_story_prompt == "None":
            return 'Story recreation skipped', 200
        story = _get_story_object()
        new_story_content = ''.join(chunk for chunk in llm_content_processor.recreate_story('\n'.join(story.parts[:3]), new_story_prompt, story.pages-3) if chunk is not None)
        story.recreate_story(new_story_content)
        story.save_as_json()
        generate_voiceover_for_next_two_pages(story)
        generate_images_for_next_two_pages(story)
        return 'Story recreation successfully', 200

@app.route("/interact", methods=["POST"])
def interact_with_ai():
    _check_story_created() # Ensure the story is created
    if app.config['dialogue'] is None:
        app.config['dialogue'] = Conversation(app.config['uuid'])
    query = request.get_json()['query']
    app.config['dialogue'].add_message('user', query)
    llm_content_processor = LLMServiceViaPortKey()
    story_of_current_progress = _get_story_object().get_current_progress_parts()
    response = ''.join(chunk for chunk in llm_content_processor.interact(app.config['dialogue'].get_conversation(), story_of_current_progress) if chunk is not None)
    app.config['dialogue'].add_message('assistant', response)
    return jsonify({'response': response})

@app.route("/current_page", methods=["GET"])
def current_page():
    _check_story_created()
    return jsonify({'story': _get_story_object().get_current_page()})

@app.route("/next_page", methods=["GET"])
def next_page():
    _check_story_created()
    response = _get_story_object().next_page()
    generate_voiceover_for_next_two_pages(_get_story_object())
    generate_images_for_next_two_pages(_get_story_object())
    return {'story': response}

@app.route("/previous_page", methods=["GET"])
def previous_page():
    _check_story_created()
    response = _get_story_object().previous_page()
    generate_voiceover_for_next_two_pages(_get_story_object())
    generate_images_for_next_two_pages(_get_story_object())
    return {'story': response}

@app.route("/recreate_story", methods=["POST"])
def recreate_story():
    _check_story_created()
    children_reponse = request.get_json()['childrenReponse']
    llm_content_processor = LLMServiceViaPortKey()
    new_story_prompt = llm_content_processor.get_new_guideline(children_reponse)
    if new_story_prompt == "None":
        return jsonify({'status': 'skip'})
    story = _get_story_object()
    new_story_content = ''.join(chunk for chunk in llm_content_processor.recreate_story('\n'.join(story.parts[:3]), new_story_prompt, story.pages-3) if chunk is not None)
    story.recreate_story(new_story_content)
    story.save_as_json()
    generate_voiceover_for_next_two_pages(story)
    generate_images_for_next_two_pages(story)
    return jsonify({'status': 'success'})

def _check_story_created():
    if app.config['uuid'] is None or not Story.check_file_exists(app.config['uuid']):
        abort(404, description="No story generated yet")

def _get_story_object():
    _check_story_created()
    return Story.load_story_from_json(app.config['uuid'])

if __name__ == "__main__":
    app.run(debug=True)