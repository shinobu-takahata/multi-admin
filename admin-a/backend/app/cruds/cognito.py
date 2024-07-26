from fastapi import FastAPI, Depends, Form, HTTPException
from fastapi.security import (
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
import httpx
from config import get_settings

app = FastAPI()

settings = get_settings()

COGNITO_ISSUER = f"https://cognito-idp.{settings.cognito_region}.amazonaws.com/{settings.cognito_pool_id}"

# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl=f"{COGNITO_ISSUER}/oauth2/authorize",
#     tokenUrl=f"https://{COGNITO_ISSUER}/oauth2/token",
# )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenData(BaseModel):
    username: Optional[str] = None


async def get_cognito_public_keys():
    async with httpx.AsyncClient() as client:
        url = f"https://cognito-idp.{settings.cognito_pool_id}.amazonaws.com/.well-known/jwks.json"
        response = await client.get(url)
        return response.json()


async def verify_cognito_token(token: str = Depends(oauth2_scheme)):
    try:
        public_keys = await get_cognito_public_keys()
        header = jwt.get_unverified_header(token)
        key = next(
            (key for key in public_keys["keys"] if key["kid"] == header["kid"]),
            None,
        )
        if key is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        payload = jwt.decode(
            token, key, algorithms=["RS256"], audience=settings.cognito_app_client_id
        )
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


class OAuth2AuthorizationCodeForm(BaseModel):
    grant_type: str = Form("authorization_code")
    client_id: str = Form(...)
    client_secret: str = Form(...)
    code: str = Form(...)
    redirect_uri: str = Form(...)


class OAuth2PasswordForm(BaseModel):
    grant_type: str = Form("password")
    client_id: str = Form(...)
    client_secret: str = Form(...)
    username: str = Form(...)
    password: str = Form(...)
    scope: str = Form("openid")
