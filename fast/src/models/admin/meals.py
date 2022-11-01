# built-ins
from uuid import uuid4

from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship, select, col

# Custom imports
from database import get_session


class MealCategories(SQLModel, table=True):
    id: str = Field(primary_key=True)
    meal_category: str
    meal_items: List["MenuItems"] = Relationship(sa_relationship_kwargs={"cascade": "delete"},
                                                 back_populates="meal_category")

    def save(self):
        with get_session() as db:
            db.add(self)
            db.commit()
            db.refresh(self)

    @staticmethod
    def fetch_all_categories():
        with get_session() as db:
            return db.exec(select(MealCategories)).fetchall()


class MenuItems(SQLModel, table=True):
    id: str = Field(primary_key=True)
    item_name: str = Field(unique=True)
    item_price: float = Field(default=0, nullable=False)
    description: str = Field(default=None, nullable=True)
    rating: float = Field(default=None, nullable=True)

    meal_category_id: Optional[str] = Field(
        default=None, foreign_key="mealcategories.id",)
    meal_category: Optional["MealCategories"] = Relationship(
        back_populates="meal_items")

    def save(self):
        with get_session() as db:
            db.add(self)
            db.commit()
            db.refresh(instance=self)

    @staticmethod
    def fetch_all_items():
        with get_session() as db:
            return db.exec(select(MenuItems)).fetchall()

    @staticmethod
    def fetch_items_by_key(key: str):
        with get_session() as db:
            return db.exec(select(MenuItems).where(col(MenuItems.item_name).ilike("%"+key+"%"))).fetchall()

    @staticmethod
    def fetch_item_by_key(key: str):
        with get_session() as db:
            return db.exec(select(MenuItems).where(col(MenuItems.item_name).ilike("%"+key+"%"))).one()
