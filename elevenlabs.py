# import ffmpeg
import requests
import json
from pydub import AudioSegment
from io import BytesIO
from icecream import ic  # Import Icecream untuk logging

class ElevenLabs:
  def __init__(self):
    self.url = "https://api.elevenlabs.io/v1/text-to-speech/Xb7hH8MSUJpSbSDYk0k2?allow_unauthenticated=1"
    self.headers = {
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7,en-GB;q=0.6',
      'cache-control': 'no-cache',
      'content-type': 'application/json',
      'origin': 'https://elevenlabs.io',
      'pragma': 'no-cache',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

  def text_to_speech(self, text):
    payload = {
      "text": text,
      "model_id": "eleven_multilingual_v2"
    }

    response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))

    if response.status_code == 200:
      return response.content  # Return MP3 content directly
    else:
      print(f"Error: {response.status_code} - {response.text}")
      return None