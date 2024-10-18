from flask import Flask, jsonify, request, abort
from model.Conversation import Conversation
from model.Story import Story
from llm_service.LLMServiceViaPortKey import LLMServiceViaPortKey


app = Flask(__name__)

# Store as global variables
app.config['story_object'] = None 
app.config['dialogue'] = Conversation()

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/generate_story", methods=["POST"])
def generate_story():
    user_input = request.get_json()
    age = user_input["age"]
    read_time = user_input["readTime"]
    elements = user_input["elements"]
    llm_content_processor = LLMServiceViaPortKey()
    story = ''.join(chunk for chunk in llm_content_processor.generate_story(age, read_time, elements) if chunk is not None)
    story_obj = Story(story)
    story_obj.title = llm_content_processor.get_story_title(story)
    story_obj.save_as_json()
    app.config['story_object'] = story_obj # serve as a global variable    
    return jsonify({'story': story})

@app.route("/get_story", methods=["GET"])
def get_story():
    _check_story_created()
    return jsonify({'story': app.config['story_object'].content,
                    'illustration_links': app.config['story_object'].illustration_links,
                    'pages': app.config['story_object'].pages})

@app.route("/interact", methods=["POST"])
def interact_with_ai():
    _check_story_created() # Ensure the story is created
    query = request.get_json()['query']
    app.config['dialogue'].add_message('user', query)
    llm_content_processor = LLMServiceViaPortKey()
    story_of_current_progress = app.config['story_object'].get_current_progress_parts()
    response = ''.join(chunk for chunk in llm_content_processor.interact(app.config['dialogue'].get_conversation(), story_of_current_progress) if chunk is not None)
    app.config['dialogue'].add_message('assistant', response)
    return jsonify({'response': response})

@app.route("/current_page", methods=["GET"])
def current_page():
    _check_story_created()
    return jsonify({'story': app.config['story_object'].get_current_page()})

@app.route("/next_page", methods=["GET"])
def next_page():
    _check_story_created()
    return jsonify({'story': app.config['story_object'].next_page()})

@app.route("/previous_page", methods=["GET"])
def previous_page():
    _check_story_created()
    return jsonify({'story': app.config['story_object'].previous_page()})

def _check_story_created():
    if app.config['story_object'] is None:
        abort(404, description="No story generated yet")

if __name__ == "__main__":
    app.run(debug=True)