from fastapi import FastAPI

# custom imports
from src.endpoints import auth

app = FastAPI()
app.include_router(auth.router)

