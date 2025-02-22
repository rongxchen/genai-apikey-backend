from fastapi import APIRouter, Depends
from src.service.api_key import APIKeyService
from src.model.api_key import APIKeyDTO
from src.model.response import success_result, failed_result
from src.util.auth import AuthUtil


router = APIRouter(
    prefix="/api/api-keys",
    tags=["API Key"],
)


@router.post("")
def add_new_api_key(api_key_dto: APIKeyDTO,
                    user_id: str = Depends(AuthUtil.get_current_user_id)):
    APIKeyService.add_one(api_key_dto, user_id=user_id)
    return success_result(message="API Key added successfully")


@router.get("")
def get_api_keys(skip: int = 0,
                 limit: int = 20,
                 user_id: str = Depends(AuthUtil.get_current_user_id)):
    data = APIKeyService.get_list(user_id, skip=skip, limit=limit)
    if data is not None:
        return success_result(data=data)
    return failed_result(message="No API key found")


@router.put("/{api_key_id}")
def update_api_key(api_key_id: str,
                   api_key_dto: APIKeyDTO,
                   user_id: str = Depends(AuthUtil.get_current_user_id)):
    APIKeyService.update_one(api_key_id, api_key_dto, user_id)
    return success_result(message="API Key updated successfully")


@router.delete("/{api_key_id}")
def delete_api_key(api_key_id: str,
                   user_id: str = Depends(AuthUtil.get_current_user_id)):
    APIKeyService.delete_one(api_key_id, user_id)
    return success_result(message="API Key deleted successfully")


@router.put("/{provider}/{api_key_id}/default")
def set_default_api_key(provider: str,
                        api_key_id: str,
                        user_id: str = Depends(AuthUtil.get_current_user_id)):
    APIKeyService.set_default(provider, api_key_id, user_id)
    return success_result(message="API Key set as default successfully")


@router.get("/providers")
def get_providers(user_id: str = Depends(AuthUtil.get_current_user_id)):
    data = APIKeyService.get_providers(user_id)
    return success_result(message="Providers fetched successfully", data=data)
