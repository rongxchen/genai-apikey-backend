import uuid


class IdUtil:
    
    def __init__(self):
        pass
    
    
    @classmethod
    def generate_id(
        cls,
        prefix: str = None, 
        remove_hyphens: bool = True
    ) -> str:
        id = str(uuid.uuid4())
        if remove_hyphens:
            id = id.replace("-", "")
        if prefix:
            id = f"{prefix}-{id}"
        return id
