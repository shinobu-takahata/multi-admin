from datetime import datetime
from pydantic import BaseModel
from schemas.schemas import ItemStatus


class Item(BaseModel):
    id: int
    name: str
    price: float
    description: str
    status: ItemStatus
    created_at: datetime
    updated_at: datetime
