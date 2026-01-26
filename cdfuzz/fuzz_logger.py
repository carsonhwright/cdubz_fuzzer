from logging import Logger

class FuzzLogger(Logger):

    def __init__(self) -> None:
        super().__init__()