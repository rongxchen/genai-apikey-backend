import asyncio
import json
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from src.util import auth_util
from src.model.response import success_result, failed_result
from src.service.chat import ChatService
from src.model.message import PromptMessageDTO


STREAM_DELAY = 1000  
RETRY_TIMEOUT = 15000

router = APIRouter(
    prefix="/api/chats",
    tags=["Chats"],
)


async def streamer():
    for i in range(100):
        yield f'data: {json.dumps({"status": "ing", "content": str(i) + "\t"})}'
        asyncio.sleep(STREAM_DELAY / 1000)
    yield f'data: {json.dumps({"status": "done"})}'


@router.post("/completion")
def prompt(request: Request,
           prompt_message_dto: PromptMessageDTO,
           user_id: str = Depends(auth_util.get_current_user_id)):
    return StreamingResponse(streamer(), headers={"Content-Type": "application/octet-stream"})


@router.get("/{chat_id}")
def get_chat(chat_id: str, 
             user_id: str = Depends(auth_util.get_current_user_id)):
    res = ChatService.get_chat(chat_id=chat_id, user_id=user_id)
    if res is None:
        return failed_result(message="Chat not found")
    return success_result(message="Chat found", data=res)


@router.get("")
def get_chats(skip: int,
              limit: int = 20, 
              user_id: str = Depends(auth_util.get_current_user_id)):
    res = ChatService.get_chats(user_id=user_id, skip=skip, limit=limit)
    return success_result(message="Chats found", data=res)


@router.get("/{chat_id}/messages")
def get_messages(chat_id: str, 
                 skip: int, 
                 limit: int = 20, 
                 user_id: str = Depends(auth_util.get_current_user_id)):
    res = ChatService.get_messages(chat_id=chat_id, user_id=user_id, skip=skip, limit=limit)
    return success_result(message="Messages found", data=res)
