from enum import Enum


class ModelName(Enum):
    ChatGPT = "chatgpt"
    DeepSeek = "deepseek"


class Model(Enum):
    ChatGPT4oMini = "gpt-4o-mini"
    DeepSeekChat = "deepseek-chat"
