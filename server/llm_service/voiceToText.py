import os
import yaml
from openai import OpenAI

def voice_to_text(audio_file_path: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), 'config', 'config.yaml'), 'r') as file:
        api_key = yaml.safe_load(file)["openai_api_key"]
    client = OpenAI(api_key=api_key)
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=open(audio_file_path, "rb")
    )
    return transcription.text