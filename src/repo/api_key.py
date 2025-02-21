from typing import Dict, List, Union
from src.repo.config.sqlite import (
    get_session,
    APIKey,
)


class APIKeyRepo:
    
    session = get_session
    
    def __init__(self):
        pass
    
    
    @classmethod
    def create_one(
        cls,
        api_key: APIKey,
    ):
        with cls.session() as session:
            session.add(api_key)
            session.commit()
    
    
    @classmethod
    def get_list(
        cls,
        user_id: str,
        skip: int,
        limit: int,
    ) -> List[APIKey]:
        with cls.session() as session:
            return session.query(APIKey).filter_by(user_id=user_id).order_by(APIKey.created_at.desc()).offset(skip).limit(limit).all()


    @classmethod
    def get_default_key(
        cls,
        provider: str,
        user_id: str
    ) -> Union[str, None]:
        with cls.session() as session:
            api_key = session.query(APIKey).filter_by(user_id=user_id, provider=provider, is_default=1).first()
            if api_key is not None:
                return api_key.key
            return None


    @classmethod
    def get_by_key(
        cls,
        key: str,
        user_id: str
    ) -> APIKey:
        with cls.session() as session:
            return session.query(APIKey).filter_by(key=key, user_id=user_id).first()


    @classmethod
    def get_by_api_key_id(
        cls,
        api_key_id: str,
        user_id: str
    ) -> APIKey:
        with cls.session() as session:
            return session.query(APIKey).filter_by(api_key_id=api_key_id, user_id=user_id).first()


    @classmethod
    def get_unique_providers(
        cls,
        user_id: str
    ) -> List[str]:
        with cls.session() as session:
            res = session.query(APIKey.provider).filter_by(user_id=user_id).distinct().all()
            return [r[0] for r in res]

    
    @classmethod
    def update(
        cls,
        update: Dict,
        **filter
    ):
        with cls.session() as session:
            session.query(APIKey).filter_by(**filter).update(update)
            session.commit()
    
    
    @classmethod
    def count(
        cls,
        **filter
    ) -> int:
        with cls.session() as session:
            return session.query(APIKey).filter_by(**filter).count()
    
    
    @classmethod
    def delete_one(
        cls,
        api_key_id: str,
        user_id: str
    ):
        with cls.session() as session:
            api_key = session.query(APIKey).filter_by(api_key_id=api_key_id, user_id=user_id).first()
            if api_key is not None:
                session.delete(api_key)
                session.commit()
    