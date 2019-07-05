from enum import Enum

class WS(Enum):

    STATUS = 'status'
    ELEMENTS = 'elements'
    SUCCESS = 'success'
    ERROR = 'error'
 
    def __str__(self):
        return str(self.value)