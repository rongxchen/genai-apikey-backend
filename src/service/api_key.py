from src.repo.api_key import APIKeyRepo
from src.model.api_key import APIKeyDTO
from src.repo.config.sqlite import APIKey
from src.util import (
    date_util,
    id_util,
    list_util,
)
from src.enum.model import ModelName
from src.exception.exception_model import InputException


class APIKeyService:
    
    provider_list = [model.value for model in ModelName]
    
    def __init__(self):
        pass
    
    
    @classmethod
    def add_one(
        cls,
        api_key_dto: APIKeyDTO,
        user_id: str
    ):
        if api_key_dto.provider not in cls.provider_list:
            raise InputException("Invalid provider")
        api_key = APIKey()
        api_key.api_key_id = id_util.generate_id()
        api_key.user_id = user_id
        api_key.provider = api_key_dto.provider
        api_key.key = api_key_dto.key
        api_key.status = 1
        api_key.created_at = date_util.get_timestamp()
        api_key.updated_at = date_util.get_timestamp()
        APIKeyRepo.create_one(api_key)


    @classmethod
    def get_list(
        cls,
        user_id: str,
        skip: int,
        limit: int
    ):
        api_keys = APIKeyRepo.get_list(user_id, skip, limit)
        if list_util.is_empty(api_keys):
            return None
        return {
            "list": api_keys,
            "size": len(api_keys),
            "has_more": len(api_keys) == limit
        }
    
    
    @classmethod
    def delete_one(
        cls,
        api_key_id: str,
        user_id: str
    ):
        APIKeyRepo.delete_one(api_key_id, user_id)
