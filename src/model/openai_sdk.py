import base64
from typing import Union


class Image:
    
    def __init__(
        self, 
        image_type: str, 
        image_data: Union[str, bytes]
    ):
        self.image_type = image_type
        self.image_data = image_data

        
    def get_image_url(
        self
    ) -> str:
        img_data = self.image_data
        if isinstance(self.image_data, bytes):
            img_data = base64.b64encode(img_data).decode("utf-8")
            return f"data:{self.image_type};base64,{img_data}"
        return self.image_data
    