from typing import Optional

from sqlalchemy.orm import Session

from domain.entities.item import Item
from domain.interfaces.item_repository import ItemRepository
from models.models import Item as ItemModel


class ItemRepositoryImpl(ItemRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_item(self, item_id: int) -> Optional[Item]:
        return self.db.query(ItemModel).filter(ItemModel.id == item_id).first()

    def create_item(self, item: Item) -> Item:
        new_item = ItemModel(**item.model_dump())
        self.db.add(new_item)
        self.db.commit()
        return new_item

    def update_item(self, item: ItemModel) -> Item:
        self.db.add(item)
        self.db.commit()
        return item

    def delete_item(self, item: ItemModel) -> None:
        self.db.delete(item)
        self.db.commit()
