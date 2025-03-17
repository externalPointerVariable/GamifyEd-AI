import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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

    def generatePodcastContent(self):
        try:
            if self.appwriteFunction.getTopic(self.topic):
                return self.appwriteFunction.getTopic(self.topic)
            else:
                content = self.generateContent()
                
                file_path = f"{self.topic}.pdf"

                with open(file_path, "wb") as file:
                    file.write(content.encode("utf-8"))

                pdfUrl = self.appwriteFunction.storePDFs(file_path)
                os.remove(file_path)
                return pdfUrl
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    pod = PodGen()
    pod.topic = "Artificial Intelligence"
    print(pod.generatePodcastContent())
