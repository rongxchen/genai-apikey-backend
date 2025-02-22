from datetime import datetime
from typing import Union


class DateUtil:
    
    def __init__(self):
        pass
    
    
    @classmethod
    def get_datetime(cls):
        return datetime.now()


    @classmethod
    def get_timestamp(
        cls,
        to_millis = True
    ) -> Union[int, float]:
        ts = cls.get_datetime().timestamp()
        if to_millis:
            ts = int(ts * 1000)
        return ts


    @classmethod
    def from_millis(
        cls,
        millis: int
    ) -> datetime:
        return datetime.fromtimestamp(millis / 1000)
