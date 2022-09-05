# Built-in
from datetime import datetime, timedelta
from pprint import pprint
from uuid import uuid4

# Framework
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Custom
from database import SessionLocal, get_db
from ..schema.auth_schema import User, LoginUser
from ..models.auth_models import Users 
from config import settings


router = APIRouter(prefix="/auth",
                   tags=["auth"],
                   )


@router.get('/')
async def index():
    return {"msg": "hello world"}


@router.post('/register')
async def create_user(data: User, db: Session = Depends(get_db)):

    user = Users.create_user(data=data, db=db)
    return {"status":"success", "msg": "user created", "username": user.username}


@router.post('/token')
async def login(data: LoginUser, db: Session = Depends(get_db)):
    user = Users.authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Users.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}