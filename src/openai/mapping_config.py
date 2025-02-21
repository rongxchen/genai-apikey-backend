from src.enum.model import Provider, Model


BASE_URL = {
    Provider.ChatGPT.value: "https://api.openai.com/v1",
    Provider.DeepSeek.value: "https://api.deepseek.com",
    Provider.SiliconFlow.value: "https://api.siliconflow.cn/v1",
}

DEFAULT_MODEL = {
    Provider.ChatGPT.value: Model.ChatGPT4oMini.value,
    Provider.DeepSeek.value: Model.DeepSeekChat.value,
    Provider.SiliconFlow.value: Model.DeepSeek_2p5.value,
}
