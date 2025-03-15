import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fastapi import APIRouter
from app.services.quizGen import quizGen


router = APIRouter()
quiz = quizGen()

@router.get("/")
def homeurl():
    return {"Message":"Welsome to the GamifyEd AI Server"}

@router.get("/api")
def listAPI():
    return {"Message":"This router provides you with the acces to use the api"}

@router.post("/api/student/quiz/{academiclevel}")
def generateStudentQuiz(academiclevel: str, topics: list[str]):
    quiz.topics = topics
    return quiz.generatePracticeQuiz(academiclevel)