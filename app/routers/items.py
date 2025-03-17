import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fastapi import APIRouter, Header
from app.services.quizGen import quizGen
from typing import Annotated
from app.model.quizModel import StudentQuiz, TeacherQuiz


router = APIRouter()
quiz = quizGen()

@router.get("/")
def homeurl():
    return {"Message":"Welsome to the GamifyEd AI Server"}

@router.get("/api")
def listAPI():
    return {"Message":"This router provides you with the acces to use the api"}

@router.post("/api/quiz/student")
def generateStudentQuiz(header:Annotated[StudentQuiz, Header()]):
    quiz.topics = header.topics
    response = quiz.generatePracticeQuiz(header.academicLevel)
    return response

@router.post("/api/quiz/teacher")
def generateTeacherQuiz(header:Annotated[TeacherQuiz, Header()]):
    quiz.topics = header.topics
    response = quiz.generateTestQuiz(header.difficulty, header.academicLevel)
    return response