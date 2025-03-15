from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def homeurl():
    return {"Message":"Welsome to the GamifyEd AI Server"}

@router.get("/api")
def listAPI():
    return {"Message":"This router provides you with the acces to use the api"}