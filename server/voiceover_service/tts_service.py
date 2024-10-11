import os
import io
from io import BytesIO
from typing import IO

from api_config import client
from elevenlabs import VoiceSettings, play, stream, save

# Optional dependencies
pydub_available = False
try:
    # Try importing pydub and its dependencies
    from pydub import AudioSegment
    from pydub.playback import play
    pydub_available = True
except ImportError:
    print("Optional dependency `pydub` is not available. `play_audio` will be disabled.")


# Raw method
def text_to_speech_stream_raw(text: str) -> IO[bytes]:
    """
    Converts text to speech and returns the audio data as a byte stream.
    Args:
        text (str): The text content to be converted into speech.
    Returns:
        IO[bytes]: A BytesIO stream containing the audio data.
    """
    # Perform the text-to-speech conversion using ElevenLabs
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Use a pre-configured voice ID
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Create a BytesIO object to hold the streamed audio data
    audio_stream = BytesIO()
    print("Streaming audio data...")

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)
    return audio_stream

# raw method
def play_audio_raw(stream: BytesIO):
    """Plays audio from a given stream if pydub is available."""
    if not pydub_available:
        raise RuntimeError("The `play_audio` function is disabled because `pydub` is not installed.")
    
    # Read the audio data into an AudioSegment object
    audio_segment = AudioSegment.from_file(stream, format="mp3")

    # Play the audio
    play(audio_segment)

#raw method call
def tts_raw():
    
    """Main function to be executed when run as a standalone script."""
    audio_stream = text_to_speech_stream_raw("Hello, world! This is using the streaming API.")
    if pydub_available:
        play_audio_raw(audio_stream)
    else:
        print("Audio playback is not available because `pydub` is not installed.")

def text_to_speech_save():
    audio = client.generate(
    text="Hello! This is a test message.",
    voice="Rachel",
    model="eleven_multilingual_v2"
    )
    save(audio,"output.mp3")

def main():
    text_to_speech_save()

if __name__ == "__main__":
    main()