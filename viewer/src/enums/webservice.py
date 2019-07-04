from enum import Enum

class WS(Enum):

    def __str__(self):
        return str(self.value)

    STATUS = 'status'
    ELEMENTS = 'elements'
    SUCCESS = 'success'
    ERROR = 'error'