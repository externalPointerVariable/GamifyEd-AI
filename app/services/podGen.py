import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import vertexai
from vertexai.preview.generative_models import GenerativeModel
import json
from app.config.config import cloudProjectId, cloudProjectLocation, playnotesApiKey, playnotesUserId
from app.utils.podrequests import getPodcastId
from app.model.appwriteFunction import AppwriteFunction

class PodGen:
    def __init__(self):
        vertexai.init(project=cloudProjectId, location=cloudProjectLocation)
        self.appwriteFunction = AppwriteFunction()
        self.topic = ""
        self.model = GenerativeModel("gemini-pro")
        self.genConfig = {"temperature": 0.8}

        self.header = {
            "AUTHORIZATION": playnotesApiKey,
            "X-USER-ID": playnotesUserId,
            "accept": "application/json",
            'Content-Type': 'application/json'
        }
        self.data = {
            'sourceFileUrl': (None, ""),
            'synthesisStyle': (None, 'podcast'),
            'voice1': (None, 's3://voice-cloning-zero-shot/65977f5e-a22a-4b36-861b-ecede19bdd65/original/manifest.json'),
            'voice1Name': (None, 'Arsenio'),
            'voice2': (None, 's3://voice-cloning-zero-shot/831bd330-85c6-4333-b2b4-10c476ea3491/original/manifest.json'),
            'voice2Name': (None, 'Nia'),
            }

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

    def generatePodcastContent(self):
        try:
            if self.appwriteFunction.getTopic(self.topic):
                print("This topic alreay exits")
                return self.appwriteFunction.getTopic(self.topic)
            else:
                content = self.generateContent()

                file_path = "generated_content.pdf" 
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)

                pdfUrl = self.appwriteFunction.storePDFs(file_path)

                os.remove(file_path)

                self.data["sourceFileUrl"] = pdfUrl
                audioUrl = getPodcastId(self.header, self.data)

                newTopic = {
                    "name": self.topic,
                    "content": content,
                    "podcasturl": audioUrl,
                }
                self.appwriteFunction.setTopic(newTopic)

                return {"content": content, "audioUrl": audioUrl}
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    pod = PodGen()
    pod.topic = "Artificial Intelligence"
    print(pod.generatePodcastContent())
