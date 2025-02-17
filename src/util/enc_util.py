import hashlib


def SHA256(text: str):
    return hashlib.sha256(text.encode()).hexdigest()


def MD5(text: str):
    return hashlib.md5(text.encode()).hexdigest()
