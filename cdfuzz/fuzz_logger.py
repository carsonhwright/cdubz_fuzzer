import logging


class FuzzLogger(logging.Logger):

    def trace(self, msg, *args, **kwargs):
        self.log(5, msg, *args, **kwargs)
    def __init__(self) -> None:
        # TODO this isn't right
        super().__init__(self)
        