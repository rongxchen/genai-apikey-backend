from enum import Enum
from typing import Union


class ModelName(Enum):
    ChatGPT = "chatgpt"
    DeepSeek = "deepseek"
    SiliconFlow = "siliconflow"


class Model(Enum):
    ChatGPT4oMini = "gpt-4o-mini"
    DeepSeekChat = "deepseek-chat"
    DeepSeek_2p5 = "deepseek-ai/DeepSeek-V2.5"


MODEL_LABEL_MAP = {
    Model.ChatGPT4oMini: "ChatGPT 4o mini",
    Model.DeepSeekChat: "DeepSeek Chat",
    Model.DeepSeek_2p5: "DeepSeek 2.5",
}


MODEL_GROUPS = {
    ModelName.ChatGPT.value: [
        {
            "model": Model.ChatGPT4oMini.value,
            "label": MODEL_LABEL_MAP[Model.ChatGPT4oMini],
        }
    ],
    ModelName.DeepSeek.value: [
        {
            "model": Model.DeepSeekChat.value,
            "label": MODEL_LABEL_MAP[Model.DeepSeekChat],
        },
    ],
    ModelName.SiliconFlow.value: [
        {
            "model": Model.DeepSeek_2p5.value,
            "label": MODEL_LABEL_MAP[Model.DeepSeek_2p5],
        }
    ],
}
