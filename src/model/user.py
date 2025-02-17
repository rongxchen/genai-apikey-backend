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
        username: str,
        email: str
    ):
        self.username = username
        self.email = email
