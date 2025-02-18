from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.exception.handler import add_exception_handler
from src.config.reader import config
from src.controller import (
    user,
    oauth2,
    api_key,
    chat,
)


app = FastAPI(
    title="Generative AI Backend",
)

app.include_router(user.router)
app.include_router(oauth2.router)
app.include_router(api_key.router)
app.include_router(chat.router)

add_exception_handler(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="app:app",
        host=config["service"]["host"],
        port=config["service"]["port"],
        reload=config["service"]["reload"],
        workers=config["service"]["workers"],
    )
