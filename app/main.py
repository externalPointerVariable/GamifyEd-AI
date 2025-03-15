import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi import FastAPI
from app.dependencies import router

app = FastAPI()
app.include_router(router)
