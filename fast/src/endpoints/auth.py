# Built-in
from src.models.auth.auth_model import Users
from config import settings
from ..schema.auth_schema import User, LoginUser
from exceptions import LoginException
from database import get_session
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT, exceptions
from fastapi import APIRouter, Depends, HTTPException, status
import sys
from datetime import datetime, timedelta
from pprint import pprint
from uuid import uuid4

sys.path.insert(0, '/home/admin/panda/fast/src')


router = APIRouter(prefix="/auth",
                   tags=["auth"],
                   )


@router.get('/')
async def index():
    return {"msg": "hello world"}


@router.post('/register')
async def create_user(data: User):
    try:
        user = Users.create_user(data=data)
        return {"op": "success", "msg": "user created", "username": user.username}
    except Exception as e:
        return {"op": "error", "msg": "user creation failed"}


# @router.post('/token')
# async def login(data: LoginUser):
#     user = Users.authenticate_user(data.username, data.password)
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
async def login(data: LoginUser, Authorize: AuthJWT = Depends()):
    try:
        user = Users.authenticate_user(data.username, data.password)
        access_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        access_token = Authorize.create_access_token(
            subject=user.username, expires_time=access_expires)
        refresh_token = Authorize.create_refresh_token(
            subject=user.username, expires_time=refresh_expires)
        return {"access_token": access_token, "refresh_token": refresh_token, "username": user.username,
                "is_caterer": user.is_caterer, "admin": user.is_admin, "op": "success"}

    except LoginException as le:
        # print(data, le)
        return {"detail": le, "op": "failed"}


@router.post('/token/refresh')
async def get_access_token_by_refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        user = Users.get_user_by_username(username=current_user)
        new_access_token = Authorize.create_access_token(subject=current_user)
        # print(user)
        # return {"access_token": new_access_token}
        return {"access_token": new_access_token, "is_caterer": user.is_caterer, "admin": user.is_admin}
    except exceptions.AuthJWTException:
        return {"msg": "Refresh token expired", "op": "failed"}
