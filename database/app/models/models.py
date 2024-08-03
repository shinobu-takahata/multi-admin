from datetime import datetime
from enum import Enum as PureEnum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ItemStatus(PureEnum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    status = Column(
        Enum(ItemStatus), nullable=False, default=ItemStatus.ON_SALE
    )
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )
    # user_id = Column(
    #     Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    # )

    # user = relationship("User", back_populates="items")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    # items = relationship("Item", back_populates="user")
