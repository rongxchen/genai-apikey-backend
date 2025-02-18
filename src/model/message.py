from pydantic import BaseModel
from typing import List, Union


# DTO
class ImageDTO(BaseModel):
    image_type: str
    image_data: str


class PromptCreateDTO(BaseModel):
    model: str


class PromptMessageDTO(BaseModel):
    chat_id: str
    content: str
    images: Union[List[ImageDTO], None] = None
    model: str
    provider: str
    

# VO
class ResponseMessageVO:
    def __init__(self, chat_id: str, message_id: str, content: str, role: str, 
                 model: str, created_at: int, updated_at: int):
        self.chat_id = chat_id
        self.message_id = message_id
        self.content = content
        self.role = role
        self.model = model
        self.created_at = created_at
        self.updated_at = updated_at
