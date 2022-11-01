# Built ins
from exceptions import LoginException
from config import settings, Settings
from src.schema.auth_schema import User
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from database import get_session
from sqlmodel import SQLModel, Field, Session, select
import sys
from datetime import datetime
from uuid import uuid4

sys.path.insert(0, '/home/admin/panda/fast/src')

# Framework
# # fastapi_jwt_auth is used instead to use both refresh and access token.


# Custom


# from typing import


# Custom config

@AuthJWT.load_config
def get_config():
    return Settings()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Users(SQLModel, table=True):
    uid: str = Field(primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    username: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    email_address: str = Field(unique=True, nullable=False)
    cell_no: str = Field(unique=True, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)
    is_caterer: bool = Field(nullable=False)
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    last_logged_in: datetime = Field(default=datetime.now())
    # TODO: Last login needs to be checked.

    def get_password_hash(password):
        return pwd_context.hash(password)

    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def create_user(data: User):

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
                         is_caterer=data.is_caterer)

        # new_user.created_at = datetime.now()
        # new_user.last_logged_in = datetime.now()

        with get_session() as db:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

    def get_user(db: Session, username: str):
        return db.exec(select(Users)).first()

    def get_user_by_username(username: str):
        with get_session() as db:
            return db.exec(select(Users).where(Users.username == username)).first()

    def authenticate_user(username: str, password: str):
        with get_session() as db:
            user = Users.get_user_by_username(username)

        if not user:
            raise LoginException("Invalid username", field="username")
        if not Users.verify_password(plain_password=password, hashed_password=user.password):
            raise LoginException("Invalid password", field="password")
        return user
