# Framework
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT, exceptions
from sqlalchemy.orm import Session

# Custom
# from database import SessionLocal, get_db
# from exceptions import LoginException
# from ..schema.auth_schema import User, LoginUser
# from ..models.auth_models import Users 
# from config import settings


router = APIRouter(prefix="/admin/meals",
                   tags=["admin", "meals"],
                   )


@router.get("/categories")
async def get_all_meal_categories():
    return {"meals": "here are all the meal categories"}