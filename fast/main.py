from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# custom imports
from src.endpoints import auth
from src.endpoints.admin import meals

origins = [
    "http://192.168.1.7:3000",
    "http://192.168.1.7:9000"
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
app.include_router(meals.router)

