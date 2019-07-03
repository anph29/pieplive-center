from . import HTTP_MODEL
from src.utils import helper

class N100_model(HTTP_MODEL):
    def __init__(self):
        super(N100_model, self).__init__()

     # POST
     # Hàm yêu cầu OTP (login) cho pieplive center
     # {
     #    NV117 :, // PiepMeID
     #    LOGIN :, // IP hoặc Mac address (của máy)
     # }
     # -1: Tai Khoan Khong Ton Tai
     # 0: Khong thanh cong
     # > 0: thanh cong
     #

    def getOtpViaNV117(self, param):
        return self.v3_post('/v3/service/plct/n2019_pieplivecenter_getOtpViaNV117_viewer', param)

    # POST
    # Hàm login cho pieplive center
    # {
    #     NV117: , // PiepmeID
    #     PV161: , // OTP (login)
    #     LOGIN: , // IP hoặc Mac address (của máy)
    # }
    # -3: Mã này đã hết hạn
    # -2: chua login app lan nao
    # -1: Dữ liệu này khong Ton Tai

    def pieplivecenterLogin(self, param):
        return self.v3_post('/v3/service/plct/n2019_pieplivecenter_login_viewer', param)
