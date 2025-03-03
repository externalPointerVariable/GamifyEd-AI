import vertexai
from vertexai.preview.generative_models import GenerativeModel
import json
from config.config import cloudProjectId, cloudProjectLocation

class quizGen:
    def __init__(self):
        self.client = vertexai.init(cloudProjectId, cloudProjectLocation)
        self.topics = []
        self.difficulties = ['Easy', 'Medium', 'Hard']
        self.model = GenerativeModel('gemini-pro')

    def generatePracticeQuiz(self):
        prompt = f'''
            Generate a quiz based on the following topics:
            {self.topics}
            and each questions should be generated with one of the following difficulties:
            {self.difficulties}
            the format in which the questions should be generated is:[
            {{
                "question:": "your question here",
                "difficulty": "assigned difficulty here",
                "options": ["option1", "option2", "option3", "option4"],
                "answer": "correct answer here",
            }}
            ]
            generate the quiz in JSON format
        '''
        response = self.model.generate_content(prompt)
        return json.loads(response)
    
    def generateTestQuiz(self, assignDifficult):
        pass
    

if __name__ == '__main__':
    quiz = quizGen()
    quiz.topics = ['Maths', 'Science', 'History']
    print(quiz.generatePracticeQuiz())