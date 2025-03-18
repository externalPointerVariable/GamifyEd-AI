import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import time
import requests
import urllib.parse
from app.config.config import playnotesApiKey, playnotesUserId


class PodcastRequest:
    def __init__(self, transcript):
        """Initialize PodcastRequest with API credentials and transcript."""
        self.headers = {
            'Authorization': playnotesApiKey,
            'X-USER-ID': playnotesUserId,
            'Content-Type': 'application/json'
        }
        self.url = "https://api.play.ai/api/v1/tts/"
        self.voice1 = 's3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json'
        self.voice2 = 's3://voice-cloning-zero-shot/e040bd1b-f190-4bdb-83f0-75ef85b18f84/original/manifest.json'
        self.transcript = transcript

    def send_request(self):
        """Send request to Play.ai API to generate the podcast."""
        payload = {
            'model': 'PlayDialog',
            'text': self.transcript,
            'voice': self.voice1,
            'voice2': self.voice2,
            'turnPrefix': 'Host 1:',
            'turnPrefix2': 'Host 2:',
            'outputFormat': 'mp3',
        }

        try:
            print("🔄 Sending request to Play.ai...")
            response = requests.post(self.url, headers=self.headers, json=payload)
            response_data = response.json()
            
            if response.status_code == 201:
                job_id = response_data.get('id')
                print(f"✅ Request successful! Job ID: {job_id}")
                return job_id
            else:
                print(f"❌ API Error: {response_data}")
                return None
        except Exception as e:
            print(f"⚠️ Exception in send_request: {e}")
            return None

    def get_audio_url(self):
        """Poll the API until the podcast generation is complete, then return the audio URL."""
        job_id = self.send_request()
        if not job_id:
            return "⚠️ Error: Could not fetch job ID."

        url = f"https://api.play.ai/api/v1/tts/{urllib.parse.quote(job_id, safe='')}"
        delay_seconds = 2

        print("⏳ Waiting for the podcast to be generated...")

        while True:
            try:
                response = requests.get(url, headers=self.headers)
                response_data = response.json()

                if response.status_code == 200:
                    status = response_data.get('output', {}).get('status')
                    print(f"🔍 Status: {status}")

                    if status == 'COMPLETED':
                        audio_url = response_data.get('output', {}).get('url')
                        return audio_url

                    elif status == 'FAILED':
                        return "❌ Podcast generation failed. Try again later."
                
                time.sleep(delay_seconds)
            except Exception as e:
                return f"⚠️ Exception in get_audio_url: {e}"


# if __name__ == '__main__':
#     # Sample podcast transcript
#     transcript = """
#     Host 1: Welcome to The Tech Tomorrow Podcast! Today we're diving into the fascinating world of voice AI and what the future holds.
#     Host 2: And what a topic this is. The technology has come so far from those early days of basic voice commands.
#     Host 1: Remember when we thought it was revolutionary just to ask our phones to set a timer?
#     Host 2: Now we're having full conversations with AI that can understand context, emotion, and even cultural nuances. It's incredible.
#     """

#     pod = PodcastRequest(transcript)
#     audio_url = pod.get_audio_url()
#     print(audio_url)
