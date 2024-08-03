from typing import Optional

from domain.entities.item import Item
from models.models import Item as ItemModel


class ItemRepository:
    def get_item(self, item_id: int) -> Optional[Item]:
        raise NotImplementedError

    def create_item(self, item: Item) -> Item:
        raise NotImplementedError

    def update_item(self, item: ItemModel) -> Item:
        raise NotImplementedError

    def delete_item(self, item: ItemModel) -> None:
        raise NotImplementedError
