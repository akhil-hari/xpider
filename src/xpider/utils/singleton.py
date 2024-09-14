class Singleton:
    def __new__(cls, *args, **kwargs):
        if hasattr(cls, "__instance__") and getattr(cls, "__instance__") is not None:
            return cls.__instance__
        else:
            setattr(cls, "__instance__", super().__new__(cls))
            return cls.__instance__
