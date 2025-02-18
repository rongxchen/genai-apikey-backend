from pydantic import BaseModel
from typing import Union


# DTO
class APIKeyDTO(BaseModel):
    provider: Union[str, None]
    key: Union[str, None]
