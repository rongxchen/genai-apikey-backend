from typing import Dict, List, Union
from src.repo.api_key import APIKeyRepo
from src.model.api_key import APIKeyDTO
from src.repo.config.sqlite import APIKey
from src.util import (
    date_util,
    id_util,
    list_util,
)
from src.enum.model import ModelName, MODEL_GROUPS
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
        if api_key_dto.provider is None or api_key_dto.key is None:
            raise InputException("Provider and key are required")
        if api_key_dto.provider not in cls.provider_list:
            raise InputException("Invalid provider")
        api_key = APIKeyRepo.get_by_key(key=api_key_dto.key, user_id=user_id)
        if api_key is not None:
            raise InputException("API key already exists")
        count = APIKeyRepo.count(user_id=user_id, provider=api_key_dto.provider)
        is_default = 1 if count == 0 else 0
        api_key = APIKey()
        api_key.api_key_id = id_util.generate_id()
        api_key.user_id = user_id
        api_key.provider = api_key_dto.provider
        api_key.key = api_key_dto.key
        api_key.status = 1
        api_key.is_default = is_default
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
            return {
                "list": [],
                "size": 0,
                "total": 0,
                "has_more": False
            }
        return {
            "list": api_keys,
            "size": len(api_keys),
            "total": APIKeyRepo.count(user_id=user_id),
            "has_more": len(api_keys) == limit
        }
        
        
    @classmethod
    def get_default_key(
        cls,
        provider: str,
        user_id: str
    ) -> Union[str]:
        key = APIKeyRepo.get_default_key(provider, user_id)
        if key is None:
            return None
        return key
        
        
    @classmethod
    def set_default(
        cls,
        provider: str,
        api_key_id: str,
        user_id: str
    ):
        APIKeyRepo.update(
            update={APIKey.is_default: 0},
            user_id=user_id, provider=provider
        )
        APIKeyRepo.update(
            update={APIKey.is_default: 1},
            user_id=user_id, provider=provider, api_key_id=api_key_id
        )
    
    
    @classmethod
    def update_one(
        cls,
        api_key_id: str,
        api_key_dto: APIKeyDTO,
        user_id: str
    ):
        updates = {}
        if api_key_dto.provider is not None:
            updates[APIKey.provider] = api_key_dto.provider
        if api_key_dto.key is not None:
            updates[APIKey.key] = api_key_dto.key
        APIKeyRepo.update(
            update=updates,
            api_key_id=api_key_id,
            user_id=user_id
        )
    
    
    @classmethod
    def delete_one(
        cls,
        api_key_id: str,
        user_id: str
    ):
        api_key = APIKeyRepo.get_by_api_key_id(api_key_id, user_id)
        if api_key is None:
            raise InputException("API key not found")
        if api_key.is_default:
            count = APIKeyRepo.count(user_id=user_id, provider=api_key.provider)
            if count > 1:
                raise InputException("Cannot delete default API key")
        APIKeyRepo.delete_one(api_key_id, user_id)


    @classmethod
    def get_providers(
        cls,
        user_id: str
    ) -> List[Dict]:
        unique_providers = APIKeyRepo.get_unique_providers(user_id)
        if list_util.is_empty(unique_providers):
            return []
        return [{
            "name": provider,
            "label": ModelName(provider).name,
            "disabled": False if provider in unique_providers else True,
            "models": list(MODEL_GROUPS[provider])
        } for provider in cls.provider_list]
