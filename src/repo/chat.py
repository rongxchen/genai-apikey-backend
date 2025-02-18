from src.repo.config.sqlite import (
    get_session,
    Chat,
)
from typing import List


class ChatRepo:
    
    session = get_session()
    
    def __init__(self):
        pass
    
    
    @classmethod
    def create_chat(
        cls,
        chat: Chat
    ):
        with cls.session as session:
            session.add(chat)
            session.commit()
    
    @classmethod
    def get_list(
        cls,
        user_id: str,
        skip: int,
        limit: int,
    ) -> List[Chat]:
        with cls.session as session:
            return session.query(Chat).filter_by(user_id=user_id).order_by(Chat.updated_at.desc()).offset(skip).limit(limit).all()
    
    
    @classmethod
    def update_chat_time(
        cls,
        chat_id: str,
        ts: int
    ):
        with cls.session as session:
            session.query(Chat).filter_by(chat_id=chat_id).update({"updated_at": ts})
            session.commit()
    
    
    @classmethod
    def delete_one(
        cls,
        chat_id: str,
        user_id: str
    ):
        with cls.session as session:
            session.query(Chat).filter_by(chat_id=chat_id, user_id=user_id).delete()
            session.commit()
    