from src.repo.message import MessageRepo
from src.util import id_util, date_util
from src.model.message import PromptCreateDTO, ResponseMessageVO, PromptMessageDTO
from typing import List
from src.repo.config.sqlite import Message
from src.enum.role import Role
from src.service.api_key import APIKeyService
from src.exception.exception_model import InputException
from src.openai.base import OpenAiModel


class ChatService:
    
    def __init__(self):
        pass
    
    
    @classmethod
    def create_chat(
        cls,
        prompt_create_dto: PromptCreateDTO
    ) -> str:
        chat_id = id_util.generate_id()
        while MessageRepo.count(chat_id=chat_id) > 0:
            chat_id = id_util.generate_id()
        return {
            "chat_id": chat_id,
            "model": prompt_create_dto.model,
        }
        
    
    @classmethod
    def prompt(
        cls,
        prompt: PromptMessageDTO,
        user_id: str
    ):
        api_key = APIKeyService.get_default_key(provider=prompt.provider, user_id=user_id)
        if api_key is None:
            raise InputException(f"No default API key found for model provider [{prompt.provider}]")
        # save user prompt
        user_prompt = Message()
        user_prompt.chat_id = prompt.chat_id
        user_prompt.message_id = id_util.generate_id()
        user_prompt.content = prompt.content
        user_prompt.role = Role.USER.value
        user_prompt.model = prompt.model
        user_prompt.user_id = user_id
        user_prompt.created_at = date_util.get_timestamp()
        user_prompt.updated_at = date_util.get_timestamp()
        # send prompt
        model = OpenAiModel(
            model_name=prompt.provider,
            api_key=api_key
        )
        res = model.prompt(prompt.content, model=prompt.model, stream=True)
        message_id = res["message_id"]
        content = res["content"]
        token_used = res["token_used"]
        # save assistant response
        model_response = Message()
        model_response.chat_id = prompt.chat_id
        model_response.message_id = message_id
        model_response.content = "".join(content) if isinstance(content, list) else content
        model_response.role = Role.ASSISTANT.value
        model_response.model = prompt.model
        model_response.user_id = user_id
        model_response.created_at = date_util.get_timestamp()
        model_response.updated_at = date_util.get_timestamp()
        user_prompt.token_used = token_used["prompt"]
        model_response.token_used = token_used["completion"]
        MessageRepo.create_one(user_prompt)
        MessageRepo.create_one(model_response)
        # for chunk in content:
        #     yield chunk


    @classmethod
    def get_messages(
        cls,
        chat_id: str,
        user_id: str,
        skip: int,
        limit: int
    ) -> List[ResponseMessageVO]:
        messages = MessageRepo.get_list(chat_id=chat_id, user_id=user_id, skip=skip, limit=limit)
        res: List[ResponseMessageVO] = []
        for message in messages:
            res.append(ResponseMessageVO(
                chat_id=message.chat_id,
                message_id=message.message_id,
                content=message.content,
                role=message.role,
                model=message.model,
                created_at=message.created_at,
                updated_at=message.updated_at
            ))
        return res
