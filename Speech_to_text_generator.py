import openai
import os
import logging
from pydub import AudioSegment

# Enable logging for debugging API requests
logging.basicConfig(level=logging.DEBUG)

# Load the API key from the environment variable
api_key = os.getenv("MY_PRIVATE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the MY_PRIVATE_API_KEY environment variable.")
openai.api_key = api_key

# Path to the audio file
audio_file = "Recordings/Call with Omer.m4a"

try:
    # Step 1: Ensure the audio file is converted to the correct format (WAV, 16kHz, mono)
    print("Converting audio file to WAV format...")
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000).set_channels(1)  # 16kHz, mono
    converted_file = "audio_sample.wav"
    audio.export(converted_file, format="wav")
    print(f"Audio file converted and saved as {converted_file}")

    # Step 2: Make the Whisper API request
    print("Sending request to Whisper API...")
    with open(converted_file, "rb") as audio:
        response = openai.Audio.transcribe("whisper-1", audio)

    # Step 3: Print the transcription result
    print("Transcription:", response['text'])

except openai.error.OpenAIError as e:
    print(f"OpenAI API Error: {e}")
except FileNotFoundError as e:
    print(f"File Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
