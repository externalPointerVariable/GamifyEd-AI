import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import requests
import json
import urllib.parse
from app.model.appwriteFunction import AppwriteFunction


def getaudioFilePath(url, header):
    try:
        response = requests.get(url, headers=header)
        if(response.status_code == 200):
            audioFilePath = response.json().get('audioFilePath')
            return audioFilePath
        else:
            return f" This error is coming from getaudioFilePath function {response.json()}"
    except Exception as e:
        return str(e)

def getPodcastId(header, data):
    try:
        url = "https://api.play.ai/api/v1/playnotes"
        response = requests.post(url, headers=header, files=data)
        if(response.status_code == 201):
            playNoteId = response.json().get('id')
            doubleEncodedId = urllib.parse.quote(playNoteId, safe='')
            finalUrl = f"https://api.play.ai/api/v1/playnotes/{doubleEncodedId}"
            audiofilePath = getaudioFilePath(finalUrl, header)
            return audiofilePath
        else:
            return f" This error is coming from getPodcastId function {response.json()}"
    except Exception as e:
        return str(e)
