import os
from api_config import client
from elevenlabs import play

# Get the relative path to the audio sample
current_dir = os.path.dirname(__file__)  # Get the directory of the current file

def clone_voice(voice_name: str, voice_description: str, voice_sample_names: list):
    relative_audio_paths = [os.path.join(current_dir, 'voice_samples', sample_name) for sample_name in voice_sample_names]  # Construct the relative paths with voice_samples folder
    # Clone the voice using the relative paths
    voice = client.clone(
        name=voice_name,
        description=voice_description,
        files=relative_audio_paths,  # Use the relative paths here
    )
    return voice


def main():
    my_voice = clone_voice("Eric", "A cloned voice", ["audio_sample.m4a"])
    audio = client.generate(text="Hi! I'm a cloned voice!", voice=my_voice)
    play(audio)

if __name__ == "__main__":
    main()