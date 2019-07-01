from src.models.http_request import HTTP_REQUEST
# from http_request import HTTP_REQUEST
from src.utils import helper


class Normal_model(HTTP_REQUEST):
    def __init__(self):
        super(Normal_model, self).__init__()

    def reset_link_stream(self, key):
        return self._get_static('https://livevn.piepme.com/control/drop/client?name='+ key)
