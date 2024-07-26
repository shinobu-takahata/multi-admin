"""
This module defines the Item and ItemStatus classes for representing items
in an inventory system.
"""

from sqlalchemy.orm import Session
from models.models import Item
from schemas.schemas import ItemCreate, ItemUpdate


def find_all(db: Session):
    return db.query(Item).all()


def find_by_id(db: Session, item_id: int, user_id: int):
    return (
        db.query(Item)
        .filter(Item.id == item_id)
        .filter(Item.user_id == user_id)
        .first()
    )


def find_by_name(db: Session, name: str):
    return db.query(Item).filter(Item.name.like(f"%{name}%")).all()


def create(db: Session, item_create: ItemCreate, user_id: int):
    new_item = Item(**item_create.model_dump(), user_id=user_id)
    db.add(new_item)
    db.commit()
    return new_item


def update(db: Session, item_id: int, item_update: ItemUpdate, user_id: int):
    item = find_by_id(db, item_id, user_id)
    if item is None:
        return None

    item.name = item.name if item_update.name is None else item_update.name
    item.price = item.price if item_update.price is None else item_update.price
    item.description = (
        item.description if item_update.description is None else item_update.description
    )
    item.status = item.status if item_update.status is None else item_update.status
    db.add(item)
    db.commit()
    return item


def delete(db: Session, item_id: int, user_id: int):
    item = find_by_id(db, item_id, user_id)
    if item is None:
        return None
    db.delete(item)
    db.commit()
    return item
