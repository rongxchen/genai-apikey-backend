from typing import Dict
from src.model.oauth2 import Token
from src.model.user import UserRegisterDTO, UserLoginDTO, UserVO
from src.repo.user import UserRepo
from src.repo.config.sqlite import User
from src.util.id import IdUtil
from src.util.enc import EncUtil
from src.util.date import DateUtil
from src.util.jwt import JwtUtil
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
        password = EncUtil.SHA256(user_dto.password + user.salt)
        if password != user.password:
            raise InputException("Password incorrect")
        token = Token(
            access_token=JwtUtil.generate_token(user_id=user.user_id),
            refresh_token=JwtUtil.generate_token(user_id=user.user_id, hours=24*30),
        )
        return token
    
    
    def register(
        user_dto: UserRegisterDTO
    ):
        user = UserRepo.get_by_email(user_dto.email)
        if user is not None:
            raise InputException("Email already exists")
        user = User()
        user.user_id = IdUtil.generate_id()
        user.email = user_dto.email
        user.username = user_dto.username
        user.salt = EncUtil.MD5(str(DateUtil.get_timestamp()))
        password = EncUtil.SHA256(user_dto.password + user.salt)
        user.password = password
        user.status = 1
        user.is_deleted = 0
        user.created_at = DateUtil.get_timestamp()
        user.updated_at = DateUtil.get_timestamp()
        UserRepo.create_one(user)
        return True
    
    
    def refresh_access_token(
        refresh_token: str
    ) -> str:
        decoded, data = JwtUtil.decode_token(refresh_token)
        if not decoded:
            raise InputException("Invalid refresh token")
        user = UserRepo.get_by_user_id(data)
        if user is None:
            raise InputException("User not found")
        return JwtUtil.generate_token(user_id=user.user_id)
    
    
    @classmethod
    def get_me(
        cls,
        user_id: str
    ) -> Dict:
        user = UserRepo.get_by_user_id(user_id=user_id)
        if user is None:
            raise InputException("User not found")
        return UserVO(
            user_id=user.user_id,
            username=user.username, 
            email=user.email
        )
    