import os
import sys
import json
from google import genai
from google.genai import types

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.config.config import googleStudioApiKey

class quizGen:
    def __init__(self):
        self.client = genai.Client(api_key=googleStudioApiKey)
        self.topics = []
        self.numberOfQuestions = 10
        self.difficulties = ['Easy', 'Medium', 'Hard']
        self.model_name = "gemini-2.0-flash"
        self.temperature = 0.8

    def _format_prompt(self, assignDifficulty=None, academicLevel="high school"):
        return f'''
        Generate {self.numberOfQuestions} multiple-choice quiz on the following topics: {self.topics}.
        {"Each question should be assigned one of the following difficulty levels: " + str(self.difficulties) + "." if not assignDifficulty else ""}
        {"Questions should be generated with assigned difficulty " + assignDifficulty + "." if assignDifficulty else ""}
        The quiz should be suitable for an {academicLevel} student.

        Each question should be structured in the following JSON format:
        Note: the questions should justify the assigned difficulty level. Do not include any questions that are too easy.
        [
            {{
                "question": "Your generated question here",
                "difficulty": "Assigned difficulty level (Easy, Medium, or Hard)",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "answer": "Correct answer from the options"
            }}
        ]
        '''
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
                model=self.model_name,
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

    def generatePracticeQuiz(self, academicLevel):
        prompt = self._format_prompt(academicLevel=academicLevel)
        response = self._generate(prompt)
        print(f"Response: {response}")
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            return f"Error parsing JSON: {e}"

    def generateTestQuiz(self, assignDifficulty, academicLevel):
        prompt = self._format_prompt(assignDifficulty=assignDifficulty, academicLevel=academicLevel)
        response = self._generate(prompt)

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            return f"Error parsing JSON: {e}"