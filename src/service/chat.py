import json
from typing import List
from src.repo.message import MessageRepo
from src.repo.chat import ChatRepo
from src.util.id import IdUtil
from src.util.date import DateUtil
from src.util.list import ListUtil
from src.model.message import ResponseMessageVO, PromptMessageDTO
from src.repo.config.sqlite import Message, Chat
from src.enum.role import Role
from src.service.api_key import APIKeyService
from src.exception.exception_model import InputException
from src.openai.base import OpenAIModel
from src.model.chat import ChatVO


class ChatService:
    
    def __init__(self):
        pass

    
    @classmethod
    def prompt(
        cls,
        prompt: PromptMessageDTO,
        user_id: str
    ):
        api_key = APIKeyService.get_default_key(provider=prompt.provider, user_id=user_id)
        if api_key is None:
            raise InputException(f"No default API key found for model provider [{prompt.provider}]")
        if prompt.chat_id is None:
            prompt.chat_id = IdUtil.generate_id()
            chat = Chat()
            chat.chat_id = prompt.chat_id
            chat.user_id = user_id
            chat.title = prompt.content
            chat.model = prompt.model
            chat.provider = prompt.provider
            chat.created_at = DateUtil.get_timestamp()
            chat.updated_at = DateUtil.get_timestamp()
            ChatRepo.create_chat(chat)
        else:
            ChatRepo.update_chat_time(chat_id=prompt.chat_id, ts=DateUtil.get_timestamp())
        # save user prompt
        user_prompt = Message()
        user_prompt.chat_id = prompt.chat_id
        user_prompt.message_id = IdUtil.generate_id()
        user_prompt.content = prompt.content
        user_prompt.role = Role.USER.value
        user_prompt.model = prompt.model
        user_prompt.user_id = user_id
        user_prompt.created_at = DateUtil.get_timestamp()
        user_prompt.updated_at = DateUtil.get_timestamp()
        user_prompt.has_think = 0
        user_prompt.think_content = ""
        # send prompt
        model = OpenAIModel(
            model_name=prompt.provider,
            api_key=api_key
        )
        msg_hist = None
        if prompt.chat_id is not None:
            msg_hist = MessageRepo.get_list(chat_id=prompt.chat_id, user_id=user_id, skip=0, limit=10)
        res = model.prompt(
            message=prompt.content, 
            model=prompt.model, 
            stream=True,
            message_history=msg_hist
        )
        message_id = res["message_id"]
        think_content = res["think_content"]
        if ListUtil.is_empty(think_content):
            think_content = ""
        else:
            think_content = "".join(think_content)
        has_think = 1 if think_content != "" else 0
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
        model_response.created_at = DateUtil.get_timestamp()
        model_response.updated_at = DateUtil.get_timestamp()
        model_response.has_think = has_think
        model_response.think_content = think_content
        user_prompt.token_used = token_used["prompt"]
        model_response.token_used = token_used["completion"]
        MessageRepo.create_one(user_prompt)
        MessageRepo.create_one(model_response)
        ChatRepo.update_chat_time(chat_id=prompt.chat_id, ts=DateUtil.get_timestamp())
        for chunk in content:
            yield f'data: {json.dumps(
                {
                    "status": "ing", 
                    "has_think": has_think,
                    "think_content": think_content,
                    "content": chunk,
                    "chat_id": prompt.chat_id,
                    "message_id": message_id
                }
            )}'
        yield f'data: {json.dumps(
            {
                "status": "done",
                "chat_id": prompt.chat_id,
                "message_id": message_id
            }
        )}'
        
        
    @classmethod
    def get_chat(
        cls,
        chat_id: str,
        user_id: str
    ) -> ChatVO:
        chat = ChatRepo.get_one(chat_id=chat_id, user_id=user_id)
        if chat is None:
            return None
        return ChatVO(
            chat_id=chat.chat_id,
            title=chat.title,
            user_id=user_id,
            model=chat.model,
            provider=chat.provider,
            created_at=chat.created_at,
            updated_at=chat.updated_at
        )
        
    
    @classmethod
    def get_chats(
        cls,
        user_id: str,
        skip: int,
        limit: int
    ) -> List[ChatVO]:
        chats = ChatRepo.get_list(user_id=user_id, skip=skip, limit=limit)
        res = []
        for chat in chats:
            res.append(ChatVO(
                chat_id=chat.chat_id,
                title=chat.title,
                user_id=user_id,
                model=chat.model,
                provider=chat.provider,
                created_at=chat.created_at,
                updated_at=chat.updated_at
            ))
        return {
            "list": res, "size": len(res), "has_more": len(res) == limit
        }


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
                updated_at=message.updated_at,
                has_think=message.has_think==1,
                think_content=message.think_content,
            ))
        return {
            "list": res, "size": len(res), "has_more": len(res) == limit
        }
        
    
    @classmethod
    def delete_chat(
        cls,
        chat_id: str,
        user_id: str
    ):
        ChatRepo.delete_one(chat_id=chat_id, user_id=user_id)
        MessageRepo.delete_by_chat_id(chat_id=chat_id)
