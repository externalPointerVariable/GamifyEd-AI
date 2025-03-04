import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import vertexai
from vertexai.preview.generative_models import GenerativeModel
import json
from app.config.config import cloudProjectId, cloudProjectLocation

class podGen:
    def __init__(self):
        self.client = vertexai.init(project=cloudProjectId, location=cloudProjectLocation)
        self.topic = ""
        self.model = GenerativeModel('gemini-pro')
        self.genConfig = {
            "temperature": 0.8,
        }

    def generateContent(self):
        try:
            prompt = f'''
                    Generate a blog content on the topic: {self.topic}.
                    The content should be at least 1900 words long.
                    format:[
                        'Main Heading',
                        'Sub Heading',
                        'Content',
                        'Conclusion',]
                    '''
            response = self.model.generate_content(prompt, generation_config=self.genConfig)
            response = response.text.strip()
            return response
        except Exception as e:
            return str(e)
        
    def generatePodcastContent(self):
        try:
            content = self.generateContent(self)
            pass
        except Exception as e:
            return str(e)
        

if __name__ == "__main__":
    pod = podGen()
    pod.topic = "Artificial Intelligence"
    print(pod.generateContent())