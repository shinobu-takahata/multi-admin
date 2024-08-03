from typing import Optional

from domain.entities.item import Item
from domain.exceptions.exception import ItemNotFoundException
from domain.services.item_service import ItemService


class ItemUseCase:
    def __init__(self, item_service: ItemService):
        self.item_service = item_service

    def get_item(self, item_id: int) -> Optional[Item]:
        try:
            return self.item_service.get_item(item_id)
        except ItemNotFoundException:
            pass

    def create_item(self, item: Item) -> Item:
        # ここで追加のビジネスロジックを実装可能
        return self.item_service.create_item(item)

    def update_item(self, item_id: int, item: Item) -> Item:
        try:
            return self.item_service.update_item(item_id, item)
        except ItemNotFoundException:
            pass

    def delete_item(self, item_id: int) -> None:
        try:
            self.item_service.delete_item(item_id)
        except ItemNotFoundException:
            pass
