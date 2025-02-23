import json
from typing import List, Union, Dict
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from src.model.message import PromptMessageDTO
from src.enum.model import Provider
from src.enum.role import Role
from src.model.openai_sdk import Image
from src.openai.mapping_config import (
    BASE_URL,
    DEFAULT_MODEL,
)
from src.repo.config.sqlite import Message
from src.repo.message import MessageRepo
from src.repo.chat import ChatRepo
from src.util.list import ListUtil
from src.util.date import DateUtil


class OpenAIModel:
    
    def __init__(
        self, 
        model_name: Union[str, Provider],
        api_key: str,
        base_url: str = None,
    ):
        if isinstance(model_name, Provider):
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
        response: Union[ChatCompletion, Stream[ChatCompletionChunk]],
        prompt: PromptMessageDTO,
        user_prompt: Message,
        model_response: Message,
    ):
        if isinstance(response, ChatCompletion):
            think_content = response.choices[0].message.reasoning_content or None
            content = response.choices[0].message.content or None
            ChatRepo.update_chat_time(chat_id=prompt.chat_id, ts=DateUtil.get_timestamp())
            yield f'data: {json.dumps(
                {
                    "status": "ing", 
                    "has_think": think_content is not None,
                    "think_content": think_content or "",
                    "content": content or "",
                    "chat_id": prompt.chat_id,
                    "message_id": response.id
                }
            )}'
            yield f'data: {json.dumps(
                {
                    "status": "done",
                    "chat_id": prompt.chat_id,
                }
            )}'
        else:
            contents = []
            think_contents = []
            for chunk in response:
                print(chunk.choices[0].delta)
                content = chunk.choices[0].delta.content
                if content is not None and content != "":
                    contents.append(content)
                think_content = chunk.choices[0].delta.reasoning_content
                if think_content is not None and think_content != "":
                    think_contents.append(think_content)
                finish_reason = chunk.choices[0].finish_reason
                if finish_reason is not None and finish_reason == "stop":
                    # user prompt
                    user_prompt.token_used = chunk.usage.prompt_tokens
                    # model response
                    model_response.message_id = chunk.id
                    model_response.token_used = chunk.usage.completion_tokens
                    if ListUtil.not_empty(contents):
                        model_response.content = ListUtil.join(contents)
                    if ListUtil.not_empty(think_contents):
                        model_response.think_content = ListUtil.join(think_contents)
                        model_response.has_think = 1
                    MessageRepo.create_one(user_prompt)
                    MessageRepo.create_one(model_response)
                    ChatRepo.update_chat_time(chat_id=prompt.chat_id, ts=DateUtil.get_timestamp())
                    yield f'data: {json.dumps(
                        {
                            "status": "done",
                            "chat_id": prompt.chat_id,
                        }
                    )}'
                    break
                else:
                    yield f'data: {json.dumps(
                        {
                            "status": "ing", 
                            "has_think": len(think_contents) > 0,
                            "think_content": think_content,
                            "content": content,
                            "chat_id": prompt.chat_id,
                            "message_id": chunk.id
                        }
                    )}'
    

    def prompt(
        self, 
        prompt_message: PromptMessageDTO,
        user_prompt: Message,
        model_response: Message,
        image: Image = None,
        stream: bool = False,
        message_history: List[Message] = None,
    ):
        req = self.__create_prompt_request(
            message=prompt_message.content,
            image=image,
            model=prompt_message.model,
            message_history=message_history
        )
        resp = self.client.chat.completions.create(
            model=req["model"],
            messages=req["messages"],
            stream=stream
        )
        return self.__handle_response(resp, prompt_message, user_prompt, model_response)
    