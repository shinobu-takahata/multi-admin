from typing import Optional

from domain.entities.item import Item
from domain.services.item_service import ItemService


class ItemUseCase:
    def __init__(self, item_service: ItemService):
        self.item_service = item_service

    def get_item(self, item_id: int) -> Optional[Item]:
        return self.item_service.get_item(item_id)

    def create_item(self, item: Item) -> Item:
        # 追加の処理を記述します。(create_itemしたあとに何かする系)
        # 例：メール送信
        return self.item_service.create_item(item)

    def update_item(self, item_id: int, item: Item) -> Item:
        return self.item_service.update_item(item_id, item)

    def delete_item(self, item_id: int) -> None:
        return self.item_service.delete_item(item_id)
