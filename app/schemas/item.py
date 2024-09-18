from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    price: float

class ItemRead(ItemBase):
    id: int
    price: float

    class Config:
        orm_mode = True
