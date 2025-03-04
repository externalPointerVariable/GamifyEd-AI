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
            "min_length": 1900,
        }

    def generateContent(self):
        try:
            prompt = f'''
                    Generate a blog content on the topic: {self.topic}.
                    The content should be at least 1900 characters long.
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
        
    def generatePodcast(self):
        try:
            pass
        except Exception as e:
            return str(e)