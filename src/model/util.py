def to_string(cls):
    def __str__(self):
        attrs = ', '.join(f"{key}={value}" for key, value in self.__dict__.items() if key not in ["_sa_instance_state"])
        return f"{self.__class__.__name__}({attrs})"
    cls.__str__ = __str__
    return cls
