from enum import Enum


class ModelName(Enum):
    ChatGPT = "chatgpt"
    DeepSeek = "deepseek"
    SiliconFlow = "siliconflow"


class Model(Enum):
    ChatGPT4oMini = "gpt-4o-mini"
    DeepSeekChat = "deepseek-chat"
    DeepSeek_2p5 = "deepseek-ai/DeepSeek-V2.5"
