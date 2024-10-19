import os
from voiceover_service.api_config import client  # Absolute import from the package
from elevenlabs import play

class VoiceCloningService:
    def __init__(self):
        # Get the directory of this file to ensure paths are relative to the module
        self.current_dir = os.path.dirname(__file__)  

    def clone_voice(self, voice_name: str, voice_description: str, voice_sample_names: list):
        """
        Clone a voice using audio samples provided.

        Args:
            voice_name (str): Name of the cloned voice.
            voice_description (str): Description for the cloned voice.
            voice_sample_names (list): List of filenames (inside voice_samples) to use for cloning.

        Returns:
            Voice: A voice object returned by the API after cloning.
        """
        # Construct the relative paths for the voice samples folder
        relative_audio_paths = [
            os.path.join(self.current_dir, 'voice_samples', sample_name) for sample_name in voice_sample_names
        ]
        
        # Clone the voice using the API
        voice = client.clone(
            name=voice_name,
            description=voice_description,
            files=relative_audio_paths,  # Pass the relative paths to the voice cloning API
        )
        return voice

    def generate_audio(self, text: str, voice):
        """
        Generate audio using a cloned voice.

        Args:
            text (str): The text to convert into speech.
            voice (Voice): The cloned voice object returned by the clone_voice method.

        Returns:
            Audio: The generated audio object from the API.
        """
        audio = client.generate(text=text, voice=voice)
        return audio

    def play_audio(self, audio):
        """
        Play the generated audio using the ElevenLabs API.

        Args:
            audio (Audio): The generated audio object to be played.
        """
        play(audio)