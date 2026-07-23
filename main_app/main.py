import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from auth_app.routes import router as auth_router
from .main_routes import  main_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(main_router, prefix="/main")

@app.get("/")
async def root():
    return {"message": "Hello World"}