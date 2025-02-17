from pydantic import BaseModel


# DTO
class APIKeyDTO(BaseModel):
    provider: str
    key: str
