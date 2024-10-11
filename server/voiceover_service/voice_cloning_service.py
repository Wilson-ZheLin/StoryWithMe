import os
from api_config import client
from elevenlabs import play

# Get the relative path to the audio sample
current_dir = os.path.dirname(__file__)  # Get the directory of the current file
relative_audio_path = os.path.join(current_dir, 'audio_sample.m4a')  # Construct the relative path

# Clone the voice using the relative path
voice = client.clone(
    name="Alex",
    description="An old American male voice with a slight hoarseness in his throat. Perfect for news",
    files=[relative_audio_path],  # Use the relative path here
)

audio = client.generate(text="Hi! I'm a cloned voice!", voice=voice)

play(audio)