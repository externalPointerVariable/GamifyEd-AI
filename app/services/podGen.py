import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import re
from google import genai
from google.genai import types
from app.utils.podrequests import PodcastRequest
from app.model.appwriteFunction import AppwriteFunction
from app.config.config import googleStudioApiKey

class PodGen:
    def __init__(self):
        self.client = genai.Client(api_key=googleStudioApiKey)
        self.appwriteFunction = AppwriteFunction()
        self.topic = ""
        self.model = "gemini-1.5-pro"
        self.temperature = 0.8

    def _generate(self, prompt):
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)],
                )
            ]

            config = types.GenerateContentConfig(
                temperature=self.temperature,
                response_mime_type="text/plain"
            )

            try:
                full_response = ""
                for chunk in self.client.models.generate_content_stream(
                    model=self.model,
                    contents=contents,
                    config=config
                ):
                    full_response += chunk.text or ""

                cleaned_response = full_response.strip().replace("```json", "").replace("```", "").replace("`", "")
                if not cleaned_response:
                    return "Error: Received empty response from Gemini API."

                return cleaned_response
            except Exception as e:
                return str(e)

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
            response = self._generate(prompt)
            if not response:
                return "Error: Received empty response from Gemini API."
            return response
        except Exception as e:
            return str(e)
        
    def generateTranscript(self, content):
        try:
            prompt =f"""
                        Generate a transscript for 4 to 5 minutes long podcast based on the following content:
                        Content:{content}
                        The transcript should be in the following format:
                        Host 1: Welcome to GamifyEd Podcasts! Today, we're diving into {self.topic}.  
                        Host 2: Absolutely, John! ...  
                    """
            response = self._generate(prompt)
            if not response:
                return "Error: Received empty response from Gemini API."
            return response
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
                print(transcript)
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


if __name__ == "__main__":
    pod = PodGen()
    pod.topic = "Hard Computing"
    print(pod.generatePodcastContent())
