from fastapi import APIRouter
from src.model.user import UserRegisterDTO
from src.model.response import success_result, failed_result
from src.service.user import UserService


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
