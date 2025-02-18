from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.util import jwt_util
from src.exception.exception_model import UnauthorizedException
from typing import Annotated


user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/oauth2/token")


def get_current_user_id(token: Annotated[str, Depends(user_oauth2_scheme)]):
    if not token:
        raise UnauthorizedException("Invalid token")
    decoded, data = jwt_util.decode_token(token)
    if not decoded: 
        if data == "token expired":
            raise UnauthorizedException(message="Token expired")
        raise UnauthorizedException(message=data)
    return data
