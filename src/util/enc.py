import hashlib


class EncUtil:
    
    def __init__(self):
        pass
    
    
    @classmethod
    def SHA256(
        cls,
        text: str
    ) -> str:
        return hashlib.sha256(text.encode()).hexdigest()


    @classmethod
    def MD5(
        cls,
        text: str
    ) -> str:
        return hashlib.md5(text.encode()).hexdigest()
