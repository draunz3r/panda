# Built-in imports
from typing import Union
from uuid import uuid4
from datetime import datetime, timedelta

# Framework imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt



# Custom imports

from database import Base
from ..schema.auth_schema import User
from config import settings

# Custom config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Users(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email_address = Column(String, unique=True, nullable=False)
    cell_no = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    is_superuser = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    last_logged_in = Column(DateTime, nullable=False)


    def get_password_hash(password):
        return pwd_context.hash(password)

    
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    def create_user(data: User, db: Session):

        hashed_password = Users.get_password_hash(data.password)
        new_user = Users(uid=str(uuid4()), 
            first_name=data.first_name, 
            last_name=data.last_name, 
            username=data.username, 
            password=hashed_password,
            email_address=data.email_address, 
            cell_no=data.cell_no, 
            is_active=data.is_active,
            is_admin=data.is_admin, 
            is_superuser=data.is_superuser)

        new_user.created_at = datetime.now()
        new_user.last_logged_in = datetime.now()
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


    def get_user(db : Session, username: str):
        return db.query(Users).filter(Users.username == username).first()


    def get_user_by_username(username: str, db : Session):
        return db.query(Users).filter(Users.username == username)


    async def get_current_user(db : Session, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            # token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = Users.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return username

    
    async def get_current_active_user(current_user: User = Depends(get_current_user)):
        if current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user


    def authenticate_user(db: Session, username: str, password: str):
        user = Users.get_user(db, username)
        if not user:
            return False
        if not Users.verify_password(password, user.password):
            return False
        return user


    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt