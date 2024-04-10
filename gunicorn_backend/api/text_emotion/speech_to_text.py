import os
from dotenv import load_dotenv
import assemblyai as aai

def transcribe_text(path):
    
    load_dotenv()
    
    aai.settings.api_key=os.environ['ASSEMBLYAI_API_KEY']

    transcriber = aai.Transcriber()
    
    transcriptions = transcriber.transcribe(path).text

    return transcriptions

# Test Case
# audio_path = "/temp_data/check_data/ebmp-test-audio.mp3"  # Absolute path
# print(transcribe_text(audio_path))