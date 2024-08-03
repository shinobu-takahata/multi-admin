from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    price: float
    description: str


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True
