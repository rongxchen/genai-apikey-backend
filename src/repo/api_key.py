from src.repo.config.sqlite import (
    get_session,
    APIKey,
)
from typing import List


class APIKeyRepo:
    
    session = get_session()
    
    def __init__(self):
        pass
    
    
    @classmethod
    def create_one(
        cls,
        api_key: APIKey,
    ):
        with cls.session as session:
            session.add(api_key)
            session.commit()
            
    
    @classmethod
    def get_list(
        cls,
        user_id: str,
        skip: int,
        limit: int,
    ) -> List[APIKey]:
        with cls.session as session:
            return session.query(APIKey).filter_by(user_id=user_id).order_by(APIKey.created_at.desc()).offset(skip).limit(limit).all()
    
    
    @classmethod
    def delete_one(
        cls,
        api_key_id: str,
        user_id: str
    ):
        with cls.session as session:
            api_key = session.query(APIKey).filter_by(api_key_id=api_key_id, user_id=user_id).first()
            if api_key is not None:
                session.delete(api_key)
                session.commit()
    