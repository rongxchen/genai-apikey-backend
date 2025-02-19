from src.model.message import PromptMessageDTO
from src.service.chat import ChatService


res = ChatService.prompt(
    prompt=PromptMessageDTO(
        chat_id=None,
        content="nice to meet u",
        model="deepseek-ai/DeepSeek-V2.5",
        provider="siliconflow",
    ),
    user_id="2ceea2b60e5c499bbe57c479fe44a2f7",
)

print(res)


# from src.repo.config.sqlite import get_session, Message, Chat
# from sqlalchemy import text

# session = get_session()

# # session.execute(text("drop table messages"))

# res = session.query(Message).all()
# for r in res:
#     print(r)