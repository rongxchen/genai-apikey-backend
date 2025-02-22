import jwt
from typing import Tuple
from src.util.date import DateUtil
from src.enum.role import Role


SEC_KEY = "7d3194f79e645c42e4396dda38be04766810ec6a00d00aced3ffc2a0a1f1a9ef"[:16]
MILLI_SECONDS_PER_HOUR = 1000 * 60 * 60


class JwtUtil:
    
    def __init__(self):
        pass
    
    
    @classmethod
    def generate_token(
        cls,
        user_id: str, 
        role: str = Role.USER.value, 
        hours: int = 2
    ) -> str:
        timestamp = DateUtil.get_timestamp()
        exp = timestamp + MILLI_SECONDS_PER_HOUR * hours
        payload = {
            "sub": user_id,
            "role": role,
            "exp": exp
        }
        token = jwt.encode(payload=payload, key=SEC_KEY, algorithm="HS256")
        return token


    @classmethod
    def decode_token(
        cls,
        token: str, 
        role: str = "user", 
        only_token_text: bool = False
    ) -> Tuple[bool, str]:
        try:
            if token.startswith("Bearer ") or only_token_text:
                token = token.replace("Bearer ", "")
            payload = jwt.decode(jwt=token, key=SEC_KEY, algorithms="HS256")
            timestamp = DateUtil.get_timestamp()
            if payload["exp"] < timestamp:
                return False, "token expired"
            if role != payload["role"]:
                return False, "unauthorized role"
            return True, payload["sub"]
        except Exception as e:
            return False, str(e)
