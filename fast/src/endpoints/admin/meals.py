# built-ins
from uuid import uuid4

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
from models.auth.auth_model import Users
from models.admin.meals import MealCategories, MenuItems
from src.schema.admin.meals_schema import MenuQuery, MenuItemSchema


router = APIRouter(prefix="/admin/meals",
                   tags=["admin", "meals"],
                   )


@router.get("/categories")
async def get_all_meal_categories(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        return {"op": "success", "msg": "fetched meal categories", "meal_cat": MealCategories.fetch_all_categories()}
    except Exception as exp:
        return {"op": "failed", "msg": "could not fetch meal categories", "meal_cat": []}


@router.post("/menuitems")
async def get_menu_from_db(key: MenuQuery, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        return {"op": "success", "msg": "fetched menu items", "items": MenuItems.fetch_items_by_key(key.key)}
    except Exception as exp:
        print(exp)
        return {"op": "failed", "msg": "could not fetch menu items", "items": []}


@router.post("/create-menu-item")
async def create_menu_item(data: MenuItemSchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        user = Users.get_user_by_username(current_user)
        if user.is_admin or user.is_caterer:
            mi = MenuItems(id=str(uuid4()), item_name=data.item_name, item_price=float(
                data.price), description=data.description)
            mi.save()

            return {"op": "success", "msg": "Successfully created menu items", "item": mi.item_name}
        else:
            return {"op": "failed", "msg": "Operation not allowed. Not enough privilege."}

    except Exception as exp:
        print("> Error occurred:{0}".format(exp))
        return {"op": "failed", "msg": "Unhandled Error Occurred", "item": data.item_name}
