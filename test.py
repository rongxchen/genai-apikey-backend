# from src.model.message import PromptMessageDTO
# from src.service.chat import ChatService


# res = ChatService.prompt(
#     prompt=PromptMessageDTO(
#         chat_id="chat_id",
#         content="hi",
#         model="deepseek-ai/DeepSeek-V2.5",
#         provider="siliconflow",
#     ),
#     user_id="2ceea2b60e5c499bbe57c479fe44a2f7",
# )

# print(res)

from src.repo.config.sqlite import get_session, Message


session = get_session()
res = session.query(Message).all()
for r in res:
    print(r)
