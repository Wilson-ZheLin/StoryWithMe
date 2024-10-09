from flask import Flask, jsonify, request
from llm_service.StoryGenerator import StoryGenerator


app = Flask(__name__)

def generate(age, read_time, elements):
    story = story_generator.generate_story(age, read_time, elements)
    return story

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/story", methods=["POST"])
def get_story():
    user_input = request.get_json()
    age = user_input["age"]
    read_time = user_input["readTime"]
    elements = user_input["elements"]
    story_generator = StoryGenerator()
    story = story_generator.generate_story(age, read_time, elements)
    return jsonify({'story': story})

if __name__ == "__main__":
    app.run(debug=True)