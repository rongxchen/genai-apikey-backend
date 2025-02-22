from pydantic import BaseModel
from typing import List, Union


# DTO
class ImageDTO(BaseModel):
    image_type: str
    image_data: str


class PromptMessageDTO(BaseModel):
    chat_id: Union[str, None] = None
    content: str
    images: Union[List[ImageDTO], None] = None
    model: str
    provider: str
    

# VO
class ResponseMessageVO:
    def __init__(self, chat_id: str, message_id: str, content: str, role: str, 
                 model: str, created_at: int, updated_at: int, has_think = False, 
                 think_content: str = ""):
        self.chat_id = chat_id
        self.message_id = message_id
        self.content = content
        self.role = role
        self.model = model
        self.created_at = created_at
        self.updated_at = updated_at
        self.has_think = has_think
        self.think_content = think_content
