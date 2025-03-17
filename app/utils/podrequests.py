import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import requests
import urllib.parse
from app.config.config import playnotesApiKey, playnotesUserId


class PodcastRequest:
    def __init__(self):
        self.headers = {
            'AUTHORIZATION': playnotesApiKey,
            'X-USER-ID': playnotesUserId,
            'accept': 'application/json'
        }
        self.url = "https://api.play.ai/api/v1/playnotes"
        self.sourcefileurl = ""
        self.files = {
            'sourceFileUrl': (None, self.sourcefileurl),
            'synthesisStyle': (None, 'podcast'),
            'voice1': (None, 's3://voice-cloning-zero-shot/baf1ef41-36b6-428c-9bdf-50ba54682bd8/original/manifest.json'),
            'voice1Name': (None, 'Angelo'),
            'voice2': (None, 's3://voice-cloning-zero-shot/e040bd1b-f190-4bdb-83f0-75ef85b18f84/original/manifest.json'),
            'voice2Name': (None, 'Deedee'),
        }

    def sendRequest(self):
        """Send a request to Play.ai API and fetch the Playnote ID."""
        try:
            print("🔄 Sending request to Play.ai...")
            print("📄 Headers:", self.headers)
            print("📁 Files:", self.files)

            response = requests.post(self.url, headers=self.headers, files=self.files)
            print("🛑 API Response:", response.text)

            if response.status_code == 201:
                playNoteId = response.json().get('id')
                print("✅ Playnote ID received:", playNoteId)
                return playNoteId
            else:
                print(f"❌ Error while fetching Playnote ID: {response.text}")
                return None
        except Exception as e:
            print(f"⚠️ Exception in sendRequest: {e}")
            return None

    def audioUrl(self):
        """Construct the audio URL using the Playnote ID."""
        audioId = self.sendRequest()

        if not audioId:
            return "⚠️ Error: Could not fetch Playnote ID."

        doubleEncodedId = urllib.parse.quote(audioId, safe='')
        constructedUrl = f"https://api.play.ai/api/v1/playnotes/{doubleEncodedId}"
        return constructedUrl


if __name__ == '__main__':
    pod = PodcastRequest()
    pod.sourcefileurl = 'https://cloud.appwrite.io/v1/storage/buckets/67c7cb790019289412ef/files/67d83040eea7603be53f/view?project=67c7cb3300089265396a'

    # Update 'sourceFileUrl' inside 'files'
    pod.files['sourceFileUrl'] = (None, pod.sourcefileurl)

    audUrl = pod.audioUrl()
    print(f"🎧 This is the audio file path: {audUrl}")
