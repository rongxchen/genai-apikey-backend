import uuid


def generate_id(prefix: str = None, remove_hyphens: bool = True):
    id = str(uuid.uuid4())
    if remove_hyphens:
        id = id.replace("-", "")
    if prefix:
        id = f"{prefix}-{id}"
    return id
