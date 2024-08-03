"""
schemas
"""

from datetime import datetime
from enum import Enum
from typing import Optional

# pyproject.tomlでpydanticのエラーが出ないようにしている
# https://github.com/pydantic/pydantic/issues/1961
from pydantic import BaseModel, ConfigDict, Field


class ItemStatus(Enum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20, examples=["Item"])
    price: int = Field(gt=0, examples=[10000])
    description: Optional[str] = Field(
        default=None, examples=["description"]
    )


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=2, max_length=20, examples=["Item"]
    )
    price: Optional[int] = Field(default=None, gt=0, examples=[10000])
    description: Optional[str] = Field(
        default=None, examples=["description"]
    )
    status: Optional[ItemStatus] = Field(
        default=None, examples=[ItemStatus.ON_SALE]
    )


class ItemResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    name: str = Field(min_length=2, max_length=20, examples=["Item"])
    price: int = Field(gt=0, examples=[10000])
    description: Optional[str] = Field(
        default=None, examples=["description"]
    )
    status: ItemStatus = Field(examples=[ItemStatus.ON_SALE])
    created_at: datetime
    updated_at: datetime
    # user_id: int

    # ORMのモデルオブジェクトを自動的に受け取り適切なレスポンススキーマに変換
    # sqlalchemyのItemクラスを返却してもこのレスポンスになる
    model_config = ConfigDict(from_attributes=True)
