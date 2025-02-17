from src.model.oauth2 import Token
from src.model.user import UserRegisterDTO, UserLoginDTO
from src.repo.user import UserRepo
from src.repo.config.sqlite import User
from src.util import (
    id_util,
    enc_util,
    date_util,
    jwt_util,
)
from src.exception.exception_model import InputException


class UserService:
    
    def __init__(self):
        pass
    
    
    def login(
        user_dto: UserLoginDTO
    ) -> Token:
        user = UserRepo.get_by_email(user_dto.email)
        if user is None:
            raise InputException("Email not found")
        password = enc_util.SHA256(user_dto.password + user.salt)
        if password != user.password:
            raise InputException("Password incorrect")
        token = Token(
            access_token=jwt_util.generate_token(user_id=user.user_id),
            refresh_token=jwt_util.generate_token(user_id=user.user_id, hours=24*30),
        )
        return token
    
    
    def register(
        user_dto: UserRegisterDTO
    ):
        user = UserRepo.get_by_email(user_dto.email)
        if user is not None:
            raise InputException("Email already exists")
        user = User()
        user.user_id = id_util.generate_id()
        user.email = user_dto.email
        user.username = user_dto.username
        user.salt = enc_util.MD5(str(date_util.get_timestamp()))
        password = enc_util.SHA256(user_dto.password + user.salt)
        user.password = password
        user.status = 1
        user.is_deleted = 0
        user.created_at = date_util.get_timestamp()
        user.updated_at = date_util.get_timestamp()
        UserRepo.create_one(user)
        return True
    
    
    def refresh_access_token(
        refresh_token: str
    ) -> str:
        decoded, data = jwt_util.decode_token(refresh_token)
        if not decoded:
            raise InputException("Invalid refresh token")
        user = UserRepo.get_by_user_id(data)
        if user is None:
            raise InputException("User not found")
        return jwt_util.generate_token(user_id=user.user_id)
    