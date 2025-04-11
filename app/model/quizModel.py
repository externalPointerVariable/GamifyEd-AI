from pydantic import BaseModel

class StudentQuiz(BaseModel):
    academicLevel:str
    topics:list[str]=[]
    numberOfQuestions:int

class TeacherQuiz(BaseModel):
    academicLevel:str
    difficulty:str
    topics:list[str]=[]
    numberOfQuestions:int