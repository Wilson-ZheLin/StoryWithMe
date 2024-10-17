import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Load environment variables from .env file
load_dotenv()

# Get API key from the environment
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set")

# Initialize the ElevenLabs API client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)