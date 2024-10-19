from flask import Flask, jsonify, request, abort
from model.Conversation import Conversation
from model.Story import Story
from llm_service.LLMServiceViaPortKey import LLMServiceViaPortKey
from util import generate_images_for_next_two_pages

app = Flask(__name__)

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
    llm_content_processor = LLMServiceViaPortKey()
    story_content = ''.join(chunk for chunk in llm_content_processor.generate_story(age, read_time, elements, hobbies, mood) if chunk is not None)
    story_obj = Story(story_content)
    app.config['uuid'] = story_obj.uuid
    story_obj.title = llm_content_processor.get_story_title(story_content)
    story_obj.save_as_json() # just to be safe
    generate_images_for_next_two_pages(story_obj)
    return jsonify({'story': "\n\n".join(story_obj.parts)})

@app.route("/get_story", methods=["GET"])
def get_story():
    _check_story_created()
    return jsonify(_get_story_object().to_dict())

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
    generate_images_for_next_two_pages(_get_story_object())
    return {'story': response}

@app.route("/previous_page", methods=["GET"])
def previous_page():
    _check_story_created()
    response = _get_story_object().previous_page()
    generate_images_for_next_two_pages(_get_story_object())
    return {'story': response}

def _check_story_created():
    if app.config['uuid'] is None or not Story.check_file_exists(app.config['uuid']):
        abort(404, description="No story generated yet")

def _get_story_object():
    _check_story_created()
    return Story.load_story_from_json(app.config['uuid'])

if __name__ == "__main__":
    app.run(debug=True)