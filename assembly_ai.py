import logging
import requests
import assemblyai as aai
from icecream import ic #for logging

class AssemblyAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.upload_url = 'https://api.assemblyai.com/v2/upload'
        
        ic(self.api_key)
        
        # Set the API key for assemblyai library
        aai.settings.api_key = self.api_key
        self.transcriber = aai.Transcriber()
        
        # Configure logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(self.__class__.__name__)

    def sound_to_text(self, transcription_url):
        config = aai.TranscriptionConfig(speech_model="nano", language_code="en")
        transcript = self.transcriber.transcribe(transcription_url, config)
        
        # Log and handle the transcription result
        if transcript.status == aai.TranscriptStatus.error:
            self.logger.error("Transcription failed with status error.")
            return None
        else:
            self.logger.info(f"Transcription text: {transcript.text}")
            return transcript.text
