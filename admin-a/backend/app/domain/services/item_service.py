import sys
from typing import Optional

# from secretstorage import ItemNotFoundException
from domain.entities.item import Item
from domain.exceptions.exception import ItemNotFoundException
from domain.interfaces.item_repository import ItemRepository


class ItemService:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    def get_item(self, item_id: int) -> Optional[Item]:
        existing_item = self.item_repository.get_item(item_id)
        if not existing_item:
            raise ItemNotFoundException("Item Not Found")

        return existing_item

    def create_item(self, item: Item) -> Item:
        return self.item_repository.create_item(item)

    def update_if_not_none(self, existing_value, new_value):
        return new_value if new_value is not None else existing_value

    def update_item(self, item_id: int, item_update: Item) -> Item:
        existing_item = self.item_repository.get_item(item_id)
        if not existing_item:
            raise ItemNotFoundException("Item Not Found")

        update_data = {
            key: self.update_if_not_none(getattr(existing_item, key), value)
            for key, value in item_update.model_dump(exclude_unset=True).items()
        }

        for key, value in update_data.items():
            setattr(existing_item, key, value)

        return self.item_repository.update_item(existing_item)

    def delete_item(self, item_id: int) -> None:
        item = self.item_repository.get_item(item_id)
        if not item:
            raise ItemNotFoundException("Item Not Found")
        self.item_repository.delete_item(item)
