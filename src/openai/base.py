import requests
from typing import Union, Dict, Callable, List
from src.enum.model import ModelName, Model
from src.enum.role import Role
from src.model.openai_sdk import Image
from src.openai.mapping_config import (
    BASE_URL
)
from src.util import (
    http_util
)


class OpenAiModel:
    
    def __init__(
        self, 
        model_name: Union[str, ModelName],
        api_key: str,
    ):
        if isinstance(model_name, ModelName):
            self.model_name = model_name.value
        else:
            self.model_name = model_name
        self.base_url = BASE_URL[self.model_name]
        self.api_key = api_key
        self.headers = {
            "User-Agent": http_util.get_user_agent(),
        }
        
    
    def __create_prompt_request(
        self, 
        message: str,
        image: Image = None
    ) -> Dict:
        default_model = ""
        if self.model_name == ModelName.ChatGPT.value:
            default_model = Model.ChatGPT4oMini.value
        res = {
            "model": default_model,
            "messages": [
                {
                    "role": Role.USER.value,
                    "content": [
                        {
                            "type": "text",
                            "text": message,
                        }
                    ]
                }
            ]
        }
        if image is not None:
            res["messages"][0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": image.get_image_url(),
                }
            })
        return res
    
    
    def __send_request(
        self, 
        req_body: Dict,
        stream: bool = False,
        to_json: bool = True
    ) -> Union[str, List]:
        path = "/chat/completion"
        resp = requests.post(
            url=f"{self.base_url}{path}",
            headers=self.headers,
            json=req_body,
            stream=stream
        )
        if stream:
            res = []
            for line in resp.iter_lines():
                line: bytes = line
                res.append(line.decode("utf-8"))
            return res
        if to_json:
            return resp.json()
        return resp.text
        
        
    def prompt(
        self, 
        message: str,
        image: Image = None,
        stream: bool = False,
        func: Callable = None,
    ) -> Union[str, None]:
        req = self.__create_prompt_request(
            message=message,
            image=image
        )
        resp = self.__send_request(req, stream=stream)
        if stream:
            for chunk in resp:
                func(chunk)
        else:
            return resp
    