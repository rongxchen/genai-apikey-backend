from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.model.response import failed_result
from src.exception.exception_model import (
    UnauthorizedException,
    InputException,
)


def add_exception_handler(app: FastAPI):
    
    @app.exception_handler(UnauthorizedException)
    def handle_unauthorized_exception(request: Request, exception: UnauthorizedException):
        return JSONResponse(
            status_code=401,
            content=failed_result(message=exception.message)
        )
    
    @app.exception_handler(InputException)
    def handle_input_exception(request: Request, exception: InputException):
        return JSONResponse(
            status_code=200,
            content=failed_result(message=exception.message)
        )
    
    @app.exception_handler(Exception)
    def handle_exception(request: Request, exception: Exception):
        return JSONResponse(
            status_code=200,
            content=failed_result(message=f"Internal server error: {exception}")
        )
    