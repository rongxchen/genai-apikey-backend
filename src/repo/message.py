from typing import List
from src.repo.config.sqlite import (
    get_session,
    Message,
)


class MessageRepo:
    
    session = get_session
    
    def __init__(self):
        pass
    
    
    @classmethod
    def create_one(
        cls,
        message: Message,
    ):
        with cls.session() as session:
            session.add(message)
            session.commit()

    
    @classmethod
    def get_list(
        cls,
        chat_id: str,
        user_id: str,
        skip: int,
        limit: int,
    ) -> List[Message]:
        with cls.session() as session:
            res = session.query(Message).filter_by(chat_id=chat_id, user_id=user_id).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()
            return res


    @classmethod
    def count(
        cls,
        **filter
    ) -> int:
        with cls.session() as session:
            res = session.query(Message).filter_by(**filter).count()
            return res


    @classmethod
    def delete_by_chat_id(
        cls,
        chat_id: str
    ):
        with cls.session() as session:
            session.query(Message).filter_by(chat_id=chat_id).delete()
            session.commit()
