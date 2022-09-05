from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    # uid: str
    first_name: str
    last_name: str
    username: str
    password: str
    email_address: str
    cell_no: str
    is_active: bool
    is_admin: bool
    is_superuser: bool
    created_at: str
    last_logged_in: str


class LoginUser(BaseModel):
    username: str
    password: str