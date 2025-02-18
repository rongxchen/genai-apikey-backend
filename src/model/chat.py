class ChatVO:
    def __init__(self, chat_id: str, title: str, user_id: str, model: str,
                 created_at: int, updated_at: int):
        self.chat_id = chat_id
        self.title = title
        self.user_id = user_id
        self.model = model
        self.created_at = created_at
        self.updated_at = updated_at
