from typing import Annotated

from cruds.cognito import TokenData, verify_cognito_token
from domain.exceptions.exception import ItemNotFoundException
from domain.services.item_service import ItemService
from fastapi import APIRouter, Depends, HTTPException
from repository.item_repository import ItemRepositoryImpl
from schemas.schemas import ItemCreate, ItemResponse, ItemUpdate
from sqlalchemy.orm import Session
from starlette import status
from use_cases.item_use_case import ItemUseCase

from database import get_db

DbDependency = Annotated[Session, Depends(get_db)]
CognitoDependency = Annotated[TokenData, Depends(verify_cognito_token)]

router = APIRouter(prefix="/items", tags=["Items"])


def get_item_use_case(db: Session = Depends(get_db)) -> ItemUseCase:
    item_service = ItemService(item_repository=ItemRepositoryImpl(db))
    return ItemUseCase(item_service)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int, use_case: ItemUseCase = Depends(get_item_use_case)
):
    try:
        item = use_case.get_item(item_id)
    except ItemNotFoundException as exc:
        raise HTTPException(
            status_code=404, detail="Item not found"
        ) from exc

    return item


@router.post(
    "", response_model=ItemResponse, status_code=status.HTTP_201_CREATED
)
async def create(
    item_create: ItemCreate,
    use_case: ItemUseCase = Depends(get_item_use_case),
):
    return use_case.create_item(item_create)


@router.put("/{item_id}", response_model=ItemResponse)
def update(
    item_id: int,
    item_update: ItemUpdate,
    use_case: ItemUseCase = Depends(get_item_use_case),
):
    try:
        item = use_case.update_item(item_id, item_update)
    except ItemNotFoundException as exc:
        raise HTTPException(
            status_code=404, detail="Item not found"
        ) from exc

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    item_id: int,
    use_case: ItemUseCase = Depends(get_item_use_case),
):
    try:
        use_case.delete_item(item_id)
    except ItemNotFoundException as exc:
        raise HTTPException(
            status_code=404, detail="Item not found"
        ) from exc

    return {}
