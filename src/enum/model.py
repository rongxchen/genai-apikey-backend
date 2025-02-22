from enum import Enum


class Provider(Enum):
    ChatGPT = "chatgpt"
    DeepSeek = "deepseek"
    SiliconFlow = "siliconflow"


class Model(Enum):
    # ChatGPT
    ChatGPT4oMini = "gpt-4o-mini"
    # DeepSeek
    DeepSeekChat = "deepseek-chat"
    DeepSeekReasoner = "deepseek-reasoner"
    # SiliconFlow
    DeepSeek_2p5 = "deepseek-ai/DeepSeek-V2.5"


MODEL_LABEL_MAP = {
    Model.ChatGPT4oMini: "ChatGPT 4o mini",
    Model.DeepSeekChat: "DeepSeek-V3 (Chat)",
    Model.DeepSeekReasoner: "DeepSeek-R1 (Reasoner)",
    Model.DeepSeek_2p5: "DeepSeek 2.5",
}


MODEL_GROUPS = {
    Provider.ChatGPT.value: [
        {
            "model": Model.ChatGPT4oMini.value,
            "label": MODEL_LABEL_MAP[Model.ChatGPT4oMini],
        }
    ],
    Provider.DeepSeek.value: [
        {
            "model": Model.DeepSeekChat.value,
            "label": MODEL_LABEL_MAP[Model.DeepSeekChat],
        },
        {
            "model": Model.DeepSeekReasoner.value,
            "label": MODEL_LABEL_MAP[Model.DeepSeekReasoner],  
        },
    ],
    Provider.SiliconFlow.value: [
        {
            "model": Model.DeepSeek_2p5.value,
            "label": MODEL_LABEL_MAP[Model.DeepSeek_2p5],
        }
    ],
}
