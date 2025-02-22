from fastapi import APIRouter, Depends
from src.model.user import UserRegisterDTO
from src.model.response import success_result, failed_result
from src.service.user import UserService
from src.util.auth import AuthUtil


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.post("/register")
def register(user_dto: UserRegisterDTO):
    success = UserService.register(user_dto)
    if success:
        return success_result(message="User registered successfully", data=success)
    return failed_result(message="User registration failed")


@router.get("/me")
def get_me(user_id: str = Depends(AuthUtil.get_current_user_id)):
    res = UserService.get_me(user_id)
    return success_result(message="User info found", data=res)
