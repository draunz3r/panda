from pydantic import BaseModel


class MenuQuery(BaseModel):
    key: str


class MenuItemSchema(BaseModel):
    item_name: str
    price: str
    description: str
