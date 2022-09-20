from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# custom imports
from src.endpoints import auth

origins = [
    "http://192.168.1.10:3000",
    "http://192.168.1.10:9000"
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

