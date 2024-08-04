from datetime import datetime
from enum import Enum as PureEnum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class ItemStatus(PureEnum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # 適切な長さを指定
    price = Column(Integer, nullable=False)
    description = Column(String(500), nullable=True)  # 適切な長さを指定
    status = Column(
        Enum(ItemStatus), nullable=False, default=ItemStatus.ON_SALE
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(DateTime, nullable=True)
    # user_id = Column(
    #     Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    # )

    # user = relationship("User", back_populates="items")




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)  # ハッシュ化されたパスワードを想定
    salt = Column(String(32), nullable=False)  # 通常、ソルトは32バイト（64文字のhex）
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # items = relationship("Item", back_populates="user")
