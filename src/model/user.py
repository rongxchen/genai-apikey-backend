from pydantic import BaseModel


# DTO
class UserLoginDTO(BaseModel):
    email: str
    password: str
    

class UserRegisterDTO(BaseModel):
    username: str
    email: str
    password: str


# VO
class UserVO:
    
    def __init__(
        self,
        user_id: str,
        username: str,
        email: str
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
