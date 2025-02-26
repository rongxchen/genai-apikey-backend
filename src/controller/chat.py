from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from src.util.auth import AuthUtil
from src.model.response import success_result, failed_result
from src.service.chat import ChatService
from src.model.message import PromptMessageDTO
from src.model.chat import ChatRenameDTO


router = APIRouter(
    prefix="/api/chats",
    tags=["Chats"],
)


@router.post("/completion")
def prompt(request: Request,
           prompt_message_dto: PromptMessageDTO,
           user_id: str = Depends(AuthUtil.get_current_user_id)):
    return StreamingResponse(ChatService.prompt(
        prompt=prompt_message_dto,
        user_id=user_id
    ), headers={"Content-Type": "application/octet-stream"})


@router.get("/{chat_id}")
def get_chat(chat_id: str, 
             user_id: str = Depends(AuthUtil.get_current_user_id)):
    res = ChatService.get_chat(chat_id=chat_id, user_id=user_id)
    if res is None:
        return failed_result(message="Chat not found")
    return success_result(message="Chat found", data=res)


@router.put("/{chat_id}")
def rename_chat_title(chat_id: str,
                      chat_rename_dto: ChatRenameDTO,
                      user_id: str = Depends(AuthUtil.get_current_user_id)):
    updated = ChatService.rename_chat_title(chat_id=chat_id, chat_rename_dto=chat_rename_dto, user_id=user_id)
    if not updated:
        return failed_result(message="Chat title not updated")
    return success_result(message="Chat title updated", data=updated)


@router.get("")
def get_chats(skip: int,
              limit: int = 20, 
              user_id: str = Depends(AuthUtil.get_current_user_id)):
    res = ChatService.get_chats(user_id=user_id, skip=skip, limit=limit)
    return success_result(message="Chats found", data=res)


@router.get("/{chat_id}/messages")
def get_messages(chat_id: str, 
                 skip: int, 
                 limit: int = 20, 
                 user_id: str = Depends(AuthUtil.get_current_user_id)):
    res = ChatService.get_messages(chat_id=chat_id, user_id=user_id, skip=skip, limit=limit)
    return success_result(message="Messages found", data=res)


@router.delete("/{chat_id}")
def delete_chat(chat_id: str, 
                user_id: str = Depends(AuthUtil.get_current_user_id)):
    ChatService.delete_chat(chat_id=chat_id, user_id=user_id)
    return success_result(message="Chat deleted")
