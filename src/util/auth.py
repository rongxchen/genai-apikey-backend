from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from src.util.jwt import JwtUtil
from src.exception.exception_model import (
    UnauthorizedException, 
    InputException
)


user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/oauth2/token")


class AuthUtil:
    
    def __init__(self):
        pass
    
    
    @classmethod
    def get_current_user_id(
        cls,
        token: Annotated[str, Depends(user_oauth2_scheme)]
    ) -> str:
        if not token:
            raise UnauthorizedException("Invalid token")
        decoded, data = JwtUtil.decode_token(token)
        if not decoded: 
            if data == "token expired":
                raise UnauthorizedException(message="Token expired")
            raise InputException(message=data)
        return data
