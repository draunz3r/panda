# Built-in
from datetime import datetime, timedelta
from pprint import pprint
from uuid import uuid4

# Framework
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT, exceptions
from sqlalchemy.orm import Session

# Custom
from database import SessionLocal, get_db
from exceptions import LoginException
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
    try:
        user = Users.create_user(data=data, db=db)
        return {"op":"success", "msg": "user created", "username": user.username}
    except Exception as e:
        return {"op": "error", "msg": "user creation failed"}


# @router.post('/token')
# async def login(data: LoginUser, db: Session = Depends(get_db)):
#     user = Users.authenticate_user(db, data.username, data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = Users.create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post('/login')
async def login(data: LoginUser, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        user = Users.authenticate_user(db, data.username, data.password)
        access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        access_token = Authorize.create_access_token(subject=user.username, expires_time=access_expires)
        refresh_token = Authorize.create_refresh_token(subject=user.username, expires_time=refresh_expires)
        return {"access_token": access_token, "refresh_token": refresh_token, "op":"success"}

    except LoginException as le:
        return {"detail" : le, "op": "failed"}


@router.post('/token/refresh')
async def get_access_token_by_refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=current_user)
        return {"access_token": new_access_token}
    except exceptions.AuthJWTException:
        return {"msg": "Refresh token expired", "op": "failed"}