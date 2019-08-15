from . import HTTP_MODEL

class Normal_model(HTTP_MODEL):
    def __init__(self):
        super(Normal_model, self).__init__()

    def reset_link_stream(self, key):
        return self._get_static('https://livevn.piepme.com/control/drop/client?name='+ key)

    def get_request_link(self, link):
        return self._get_static(link)
