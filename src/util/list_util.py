from typing import List


def is_empty(lst: List):
    if lst is None or len(lst) == 0:
        return True
    return False


def not_empty(lst: List):
    return not is_empty(lst)
