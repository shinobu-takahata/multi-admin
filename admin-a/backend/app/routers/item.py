from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from cruds import item, auth as auth_crud

from cruds.cognito import TokenData, verify_cognito_token
from database import get_db
from routers.auth import get_user
from schemas.schemas import ItemCreate, ItemResponse, ItemUpdate
from schemas.userschema import DecodedToken

# from cruds.jwk import jwks

DbDependency = Annotated[Session, Depends(get_db)]
UserDependency = Annotated[DecodedToken, Depends(auth_crud.get_current_user)]
CognitoDependency = Annotated[TokenData, Depends(verify_cognito_token)]

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", response_model=list[ItemResponse])
async def find_all(db: DbDependency, user: dict = Depends(get_user)):
    return item.find_all(db)


# @router.get("/{item_id}", response_model=ItemResponse)
# async def find_by_id(db: DbDependency, user: UserDependency, item_id: int = Path(gt=0)):
#     found_item = item.find_by_id(db, item_id, user.user_id)
#     if not found_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return found_item


# @router.get("/", response_model=list[ItemResponse])
# async def find_by_name(
#     db: DbDependency, name: str = Query(min_length=2, max_length=20)
# ):
#     return item.find_by_name(db, name)


# @router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
# async def create(db: DbDependency, user: UserDependency, item_create: ItemCreate):
#     return item.create(db, item_create, user.user_id)


# @router.put("/{item_id}", response_model=ItemResponse)
# async def update(
#     db: DbDependency,
#     user: UserDependency,
#     item_update: ItemUpdate,
#     item_id: int = Path(gt=0),
# ):
#     updated_item = item.update(db, item_id, item_update, user.user_id)
#     if not updated_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return updated_item


# @router.delete("/{item_id}", response_model=ItemResponse)
# async def delete(db: DbDependency, user: UserDependency, item_id: int = Path(gt=0)):
#     deleted_item = item.delete(db, item_id, user.user_id)
#     if not deleted_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return deleted_item
