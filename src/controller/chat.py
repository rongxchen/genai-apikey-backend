from fastapi import APIRouter, Depends
from src.util import auth_util
from src.model.response import success_result
from src.service.chat import ChatService


router = APIRouter(
    prefix="/api/chats",
    tags=["Chats"],
)


@router.get("")
def get_chats(skip: int,
              limit: int = 20, 
              user_id: str = Depends(auth_util.get_current_user_id)):
    res = ChatService.get_chats(user_id=user_id, skip=skip, limit=limit)
    return success_result(message="Chats found", data=res)


@router.get("/messages")
def get_messages(chat_id: str, 
                 skip: int, 
                 limit: int = 20, 
                 user_id: str = Depends(auth_util.get_current_user_id)):
    res = ChatService.get_messages(chat_id=chat_id, user_id=user_id, skip=skip, limit=limit)
    return success_result(message="Messages found", data=res)
