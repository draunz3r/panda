from pydantic import BaseModel
from typing import List, Optional


class MenuQuery(BaseModel):
    key: str


class MenuItemSchema(BaseModel):
    item_name: str
    price: str
    description: str


class MealCategorySchema(BaseModel):
    category: str
    menuItems: List[str]
