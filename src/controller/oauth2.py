from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.exception.exception_model import InputException
from src.model.user import UserLoginDTO
from src.service.user import UserService
from src.enum.oauth2 import GrantType
from src.model.oauth2 import OAuth2RequestBody, Token


router = APIRouter(
    prefix="/api/oauth2", 
    tags=["OAuth2"]
)


@router.post("/token")
def get_token_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dto = UserLoginDTO(email=form_data.username, password=form_data.password)
    token = UserService.login(user_dto)
    return token


@router.post("/refresh-token")
def refresh_token(form_data: OAuth2RequestBody) -> Token:
    if not form_data.grant_type:
        raise InputException("Grant type is required")
    if form_data.grant_type == GrantType.REFRESH_TOKEN.value:
        if not form_data.refresh_token:
            raise InputException("Refresh token is required")
        access_token = UserService.refresh_access_token(form_data.refresh_token)
        return Token(access_token=access_token)
    raise InputException("Invalid grant type for OAuth2")
