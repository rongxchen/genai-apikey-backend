from typing import List, Union, Dict
from src.enum.model import ModelName
from src.enum.role import Role
from src.model.openai_sdk import Image
from src.openai.mapping_config import (
    BASE_URL,
    DEFAULT_MODEL,
)
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from src.repo.config.sqlite import Message


class OpenAIModel:
    
    def __init__(
        self, 
        model_name: Union[str, ModelName],
        api_key: str,
        base_url: str = None,
    ):
        if isinstance(model_name, ModelName):
            self.model_name = model_name.value
        else:
            self.model_name = model_name
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = BASE_URL[self.model_name]
        self.api_key = api_key
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
    
    def __create_prompt_request(
        self, 
        message: str,
        image: Image = None,
        model: str = None,
        message_history: List[Message] = None
    ) -> Dict:
        if model is None:
            default_model = DEFAULT_MODEL[self.model_name]
        else:
            default_model = model
        res = {
            "model": default_model,
            "messages": []
        }
        if image is not None:
            res["messages"][0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": image.get_image_url(),
                }
            })
        if message_history is not None:
            for _message in message_history:
                res["messages"].append({
                    "role": _message.role,
                    "content": [
                        {
                            "type": "text",
                            "text": _message.content,
                        }
                    ]
                })
        res["messages"].append({
            "role": Role.USER.value,
            "content": [
                {
                    "type": "text",
                    "text": message,
                }
            ]
        })
        return res
    
    
    def __handle_response(
        cls,
        response: Union[ChatCompletion, Stream[ChatCompletionChunk]]
    ) -> Dict[str, Union[str, List[str]]]:
        if isinstance(response, ChatCompletion):
            return {
                "message_id": response.id,
                "content": response.choices[0].message.content,
                "token_used": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                }
            }
        else:
            resp = []
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content is not None and content != "":
                    resp.append(content)
                finish_reason = chunk.choices[0].finish_reason
                if finish_reason is not None and finish_reason == "stop":
                    return {
                        "message_id": chunk.id,
                        "content": resp,
                        "token_used": {
                            "prompt": chunk.usage.prompt_tokens,
                            "completion": chunk.usage.completion_tokens,
                            "total": chunk.usage.total_tokens
                        }
                    }
    

    def prompt(
        self, 
        message: str,
        image: Image = None,
        stream: bool = False,
        model: str = None,
        message_history: List[Message] = None
    ) -> Dict[str, Union[str, List[str]]]:
        req = self.__create_prompt_request(
            message=message,
            image=image,
            model=model,
            message_history=message_history
        )
        resp = self.client.chat.completions.create(
            model=req["model"],
            messages=req["messages"],
            stream=stream
        )
        return self.__handle_response(resp)
    