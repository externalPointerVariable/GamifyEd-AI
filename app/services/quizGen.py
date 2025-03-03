import vertexai
from vertexai.preview.generative_models import GenerativeModel
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config.config import cloudProjectId, cloudProjectLocation

class quizGen:
    def __init__(self):
        self.client = vertexai.init(project=cloudProjectId, location=cloudProjectLocation)
        self.topics = []
        self.difficulties = ['Easy', 'Medium', 'Hard']
        self.model = GenerativeModel('gemini-pro')
        self.genConfig = {
            "temperature": 0.8,
        }

    def generatePracticeQuiz(self, academicLevel):
        try:
            prompt = f'''
                    Generate a multiple-choice quiz on the following topics: {self.topics}.  
                    Each question should be assigned one of the following difficulty levels: {self.difficulties}.  
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
            response = self.model.generate_content(prompt, generation_config=self.genConfig)
            response = response.text.strip()
            return json.dumps(response)
        except Exception as e:
            return str(e)
    
    def generateTestQuiz(self, assignDifficulty, academicLevel):
        try:
            prompt =f'''
                    Generate a multiple-choice quiz on the following topics: {self.topics}.  
                    Questions should be generated with assigned difficulty {assignDifficulty}.  
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
            response = self.model.generate_content(prompt, generation_config=self.genConfig)
            response = response.text.strip()
            return json.dumps(response)
        except Exception as e:
            return str(e)
    
