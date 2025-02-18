from src.enum.model import ModelName, Model


BASE_URL = {
    ModelName.ChatGPT.value: "https://api.openai.com/v1",
    ModelName.DeepSeek.value: "https://api.deepseek.com",
    ModelName.SiliconFlow.value: "https://api.siliconflow.cn/v1",
}

DEFAULT_MODEL = {
    ModelName.ChatGPT.value: Model.ChatGPT4oMini.value,
    ModelName.DeepSeek.value: Model.DeepSeekChat.value,
    ModelName.SiliconFlow.value: Model.DeepSeek_2p5.value,
}
