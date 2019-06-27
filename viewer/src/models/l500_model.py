from src.utils.http_request import HTTP_REQUEST
# from http_request import HTTP_REQUEST
from src.utils import helper


class L500_model(HTTP_REQUEST):
    def __init__(self):
        super(L500_model, self).__init__()

    def l2019_listoftabL500_prov(self, param):
        return self._get('/v2/service/l500/l2019_listoftabL500_prov', param)

    # /**
    #      * POST
    #      * Lưu thông tin CAMERA
    #      * {
    #      *      FO100: , // ID Owner
    #      *      LV501: , // Name CAMERA (Note)
    #      *      LV502: , // IP
    #      *      LV503: , // Username
    #      *      LV504: , // Password
    #      *      LV505: , // Port
    #      *      LV506: , // Full link RTSP (Hoặc link Play của RTMP <: TH áp dụng cho BTV)
    #      *      LV507: , // Link RTMP Stream
    #      *      LN508: , // Type CAM (0: Cam cố định, 1: Cam của Biên Tập Viên)
    #      *      FO100M: ,// ID của member (BTV)
    #      *      LOGIN
    #      * }
    #      */


if __name__ == '__main__':
    l500 = L500_model()
    xxx = l500.l2019_listoftabL500_prov({
        'FO100': 1932,  # ID của DN
        'FO100M': 0,  # ID của member (BTV)
        'PL500': 0,  # ID Link
        'SORT': 1,  # 1: Cũ nhất, -1: Mới nhất
        'OFFSET': 0,
        'LIMIT': 20,
        'LOGIN': 'Ân'
    })

    print(xxx)
