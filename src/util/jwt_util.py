import jwt
from src.util import date_util
from src.enum.role import Role


SEC_KEY = "3e19b8c66755a3e5f61782870fdbb3a2913ce518f6028d6b247a7020fbb179d3"[:16]
MILLI_SECONDS_PER_HOUR = 1000 * 60 * 60


def generate_token(user_id: str, role: str = Role.USER.value, hours: int = 2) -> str:
    timestamp = date_util.get_timestamp()
    exp = timestamp + MILLI_SECONDS_PER_HOUR * hours
    payload = {
        "sub": user_id,
        "role": role,
        "exp": exp
    }
    token = jwt.encode(payload=payload, key=SEC_KEY, algorithm="HS256")
    return token


def decode_token(token: str, role: str = "user", only_token_text: bool = False):
    try:
        if token.startswith("Bearer ") or only_token_text:
            token = token.replace("Bearer ", "")
        payload = jwt.decode(jwt=token, key=SEC_KEY, algorithms="HS256")
        timestamp = date_util.get_timestamp()
        if payload["exp"] < timestamp:
            return False, "token expired"
        if role != payload["role"]:
            return False, "unauthorized role"
        return True, payload["sub"]
    except Exception as e:
        return False, str(e)
