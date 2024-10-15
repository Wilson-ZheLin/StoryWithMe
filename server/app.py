from flask import Flask, jsonify, request, abort
from model.Conversation import Conversation
from model.Story import Story
from llm_service.LLMServiceViaPortKey import LLMServiceViaPortKey


app = Flask(__name__)

# Store as global variables
app.config['story_object'] = None 
app.config['dialogue'] = Conversation()

# def generate(age, read_time, elements):
#     story = story_generator.generate_story(age, read_time, elements)
#     return story

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/generate_story", methods=["POST"])
def generate_story():
    user_input = request.get_json()
    age = user_input["age"]
    read_time = user_input["readTime"]
    elements = user_input["elements"]
    # story_generator = StoryGenerator()
    # story = story_generator.generate_story(age, read_time, elements)
    llm_content_processor = LLMServiceViaPortKey()
    story = ''.join(chunk for chunk in llm_content_processor.generate_story(age, read_time, elements) if chunk is not None)
    app.config['story_object'] = Story(story) # serve as a global variable
    return jsonify({'story': story})

@app.route("/interact", methods=["POST"])
def interact_with_ai():
    _check_story_created()
    query = request.get_json()['query']
    app.config['dialogue'].add_message('user', query)
    llm_content_processor = LLMServiceViaPortKey()
    story_of_current_progress = ' '.join(app.config['story_object'].parts[:app.config['story_object'].cursor+1])
    response = ''.join(chunk for chunk in llm_content_processor.interact(app.config['dialogue'].get_conversation(), story_of_current_progress) if chunk is not None)
    app.config['dialogue'].add_message('assistant', response)
    return jsonify({'response': response})

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