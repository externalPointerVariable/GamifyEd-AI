import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import re
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from app.config.config import cloudProjectId, cloudProjectLocation
from app.utils.podrequests import PodcastRequest
from app.model.appwriteFunction import AppwriteFunction

class PodGen:
    def __init__(self):
        vertexai.init(project=cloudProjectId, location=cloudProjectLocation)
        self.appwriteFunction = AppwriteFunction()
        self.topic = ""
        self.model = GenerativeModel("gemini-pro")
        self.genConfig = {"temperature": 0.8}


    def generateContent(self):
        try:
            prompt = f"""
                Generate a blog content on the topic: {self.topic}.
                The content should be at least 1900 words long.
                Format:
                - Main Heading
                - Sub Heading
                - Content
                - Conclusion
            """
            response = self.model.generate_content(prompt, generation_config=self.genConfig)
            return response.text.strip()
        except Exception as e:
            return str(e)
        
    def generateTranscript(self, content):
        try:
            prompt =f"""
                        Generate a transscript for 4 to 5 minutes long podcast based on the following content:
                        Content:{content}
                        The transcript should be in the following format:
                        Host 1: Line from Host 1
                        Host 2: Line from Host 2
                    """
            response = self.model.generate_content(prompt, generation_config=self.genConfig)
            return response.text.strip()
        except Exception as e:
            return str(e)
        
    def removeMarkdown(self,text):
         text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
         text = re.sub(r"(\*|_)(.*?)\1", r"\2", text)
         text = re.sub(r"`(.*?)`", r"\1", text)
         lines = text.strip().split("\n")
         if len(lines)>3:
             text = "\n".join(lines[2:-1])
         else:
             text=""
         return text

    def generatePodcastContent(self):
        try:
            if self.appwriteFunction.getTopic(self.topic):
                return self.appwriteFunction.getTopic(self.topic)
            else:
                content = self.generateContent()
                transcript = self.generateTranscript(content)
                transcript = self.removeMarkdown(transcript)
                pod = PodcastRequest(transcript)
                audioUrl = pod.get_audio_url()
                newTopic = {
                    "name":self.topic,
                    "content":content,
                    "podcasturl":audioUrl
                }
                response = self.appwriteFunction.setTopic(newTopic)
                return response
        except Exception as e:
            return str(e)


# if __name__ == "__main__":
#     pod = PodGen()
#     pod.topic = "Computer Vision"
#     print(pod.generatePodcastContent())
