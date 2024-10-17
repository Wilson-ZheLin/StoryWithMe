import os
import io
from io import BytesIO
from typing import IO
import typing,json

from api_config import client
from elevenlabs import VoiceSettings, play, stream, save
from elevenlabs.types.voice import Voice

SESSION_FILE = os.path.join("server", "voiceover_service","sessions.json")

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


def load_session_data() -> dict:
    """Loads the session metadata from the JSON file."""
    if not os.path.exists(SESSION_FILE):
        # If the file doesn't exist, return an empty dictionary
        return {}

    try:
        with open(SESSION_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        # If the file is empty or has invalid JSON, return an empty dictionary
        print(f"Warning: {SESSION_FILE} contains invalid JSON. Resetting session data.")
        return {}

def save_session_data(session_data: dict):
    """Saves the session metadata to the JSON file."""
    with open(SESSION_FILE, 'w') as file:
        json.dump(session_data, file, indent=4)

def get_next_session_id(session_data: dict) -> str:
    """Determines the next session ID based on the metadata file."""
    if not session_data:
        return 'session_001'
    
    last_session_id = max(session_data.keys())
    last_session_number = int(last_session_id.split('_')[-1])
    next_session_number = last_session_number + 1
    return f'session_{next_session_number:03d}'

def text_to_speech_save(
    session_texts: list[str] = ["Hello! This is a test message."],
    voice: typing.Union[str, Voice] = "Rachel",
    model: str = "eleven_multilingual_v2",
    output_dir: str = os.path.join("server", "voiceover_service", "voice_output")
) -> list[str]:
    """
    Converts a list of texts to speech and saves the audio files in an auto-incremented session-specific folder.
    Tracks the sessions using a JSON metadata file.
    
    Args:
        session_texts (list[str]): The list of text contents to be converted into speech.
        voice (Union[str, Voice]): The voice ID or Voice object to be used for the conversion.
        model (str): The model ID to be used for the conversion.
        output_dir (str): The base directory where session folders will be created.
        
    Returns:
        list[str]: A list of relative file paths to the saved audio files for the current session.
    """
    # Load session metadata
    session_data = load_session_data()

    # Determine the next session ID
    session_id = get_next_session_id(session_data)
    
    # Create the session directory
    session_dir = os.path.join(output_dir, session_id)
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    # Handle if the voice is passed as a Voice object or string
    voice_id = voice.voice_id if isinstance(voice, Voice) else voice

    # Generate and save audio files, and track paths for this session
    audio_paths = []
    for i, text in enumerate(session_texts):
        # Generate speech using the provided voice and model
        audio = client.generate(
            text=text,
            voice=voice_id,
            model=model
        )
        # Save the audio file
        output_file = os.path.join(session_dir, f"audio_{i}.mp3")
        save(audio, output_file)
        # Append the relative path (relative to the output_dir)
        relative_path = os.path.relpath(output_file, output_dir)
        audio_paths.append(relative_path)
    
    # Update session metadata
    session_data[session_id] = {
        'session_texts': session_texts,
        'audio_paths': audio_paths,
        'voice': voice_id,
        'model': model
    }
    
    # Save the updated session metadata
    save_session_data(session_data)

    return audio_paths

def main():
    from voice_cloning_service import clone_voice
    # my_voice = clone_voice("Eric-1", "A cloned voice", ["audio_sample.m4a"])
    audio_path = text_to_speech_save(session_texts=["Have a good day", "This is a test message"], voice="Eric-1")
    print(audio_path)

if __name__ == "__main__":
    main()