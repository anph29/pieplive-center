from . import HTTP_MODEL


class Socket_model(HTTP_MODEL):
    def __init__(self):
        super(Socket_model, self).__init__()

    # POST
    # Ham gui dum pieplivecenter qua socket
    # {
    #     event, // 
    #     data, // 
    #     LOGIN
    # }
    # tokenV3
    # app.route('/v3/service/plct/ws2019_sendToSocket')
    def send_notify_piep(self, param):
        return self.v3_post("/v3/service/plct/ws2019_sendToSocket", param)
