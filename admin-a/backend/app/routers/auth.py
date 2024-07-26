import base64
import hashlib
import hmac
import boto3
from jose import JWTError, jwt
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import httpx
from sqlalchemy.orm import Session
from starlette import status
from config import get_settings
from cruds import auth as auth_crud

from schemas.userschema import Token, UserCreate, UserResponse
from database import get_db
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["auth"])
DbDependency = Annotated[Session, Depends(get_db)]
FormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]

# Cognito設定
# Cognito設定
settings = get_settings()
COGNITO_ISSUER = f"https://cognito-idp.{settings.cognito_region}.amazonaws.com/{settings.cognito_pool_id}"
client = boto3.client(
    "cognito-idp",
    region_name=settings.cognito_region,

)

# @router.post(
#     "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
# )
# async def signup(db: DbDependency, user_create: UserCreate):
#     return auth_crud.create_user(db, user_create)


# @router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
# async def login(db: DbDependency, formdata: FormDependency):
#     user = auth_crud.authenticate_user(db, formdata.username, formdata.password)
#     if not user:

#         raise HTTPException(status_code=401, detail="Invalid username or password")

#     token = auth_crud.create_access_token(user.username, user.id, timedelta(minutes=20))
#     return {"access_token": token, "token_type": "bearer"}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_user(token: str = Depends(oauth2_scheme)):
    try:
        # Tokenのデコードと検証
        # decoded_token = jwt.decode(token, options={"verify_signature": False})
        user = client.get_user(AccessToken=token)
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        response = client.initiate_auth(
            ClientId=settings.cognito_app_client_id,
            # ClientId="1ophjksllaukpj64i9vrcl3f37",
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": form_data.username,
                "PASSWORD": form_data.password,
            },
        )

        # 必要があれば別APIでこれを行う必要がある
        # response = client.respond_to_auth_challenge(
        #     ClientId=settings.cognito_app_client_id,
        #     ChallengeName=response["ChallengeName"],
        #     Session=response["Session"],
        #     ChallengeResponses={
        #         "NEW_PASSWORD": form_data.password,
        #         "USERNAME": form_data.username,
        #     },
        # )

        access_token = response["AuthenticationResult"]["AccessToken"]
        return {"access_token": access_token, "token_type": "bearer"}
    except client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    except client.exceptions.UserNotFoundException:
        raise HTTPException(status_code=400, detail="User does not exist")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
