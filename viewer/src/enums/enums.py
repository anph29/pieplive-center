from enum import Enum

class MediaType(Enum):
    CAMERA      = 1
    IMAGE       = 2
    VIDEO       = 3
    PRESENTER   = 4
    SCHEDULE    = 5
    
class MediaProp(Enum):
    ID          = 'id'
    NAME        = 'name'
    URL         = 'url'
    TYPE        = 'type'
    DURATION    = 'duration'