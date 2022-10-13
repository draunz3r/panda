from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship


class MenuItems(SQLModel, table=True):
    id:str = Field(primary_key=True)
    item_name:str
    item_price:float
    rating:float

    meal_category: Optional["MealCategories"] = Relationship(back_populates="meal_item")


class MealCategories(SQLModel, table=True):
    id:str = Field(primary_key=True)
    meal_category:str 
    meal_item: List["MenuItems"] = Relationship(back_populates="")