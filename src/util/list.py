from typing import List


class ListUtil:
    
    def __init__(self):
        pass
    
    
    @classmethod
    def is_empty(
        cls,
        lst: List
    ) -> bool:
        if lst is None or len(lst) == 0:
            return True
        return False


    @classmethod
    def not_empty(
        cls,
        lst: List
    ) -> bool:
        return not cls.is_empty(lst)
