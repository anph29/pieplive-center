from . import HTTP_MODEL


class L300_model(HTTP_MODEL):
    def __init__(self):
        super(L300_model, self).__init__()

    # POST
    # {
    #   FO100: // fo100 doanh nghiep
    #   PN303 //
    #   LV302 //IP
    #   LV303 // phone
    #   POS // vị trí camera, nếu insert L300 cho camera
    #   FT300
    #   PL300 // nếu đã có FL300 (đã lấy key) thì truyền lại FL300, (p300.PO322.live.FL300)
    #   ADDRESS
    #   LAT
    #   LONG
    #   UUID // UUID của thiết bị mobile
    #   NV124 // Quốc Gia
    #   pvLOGIN
    # }

    def updatetabP300_prov(self, param):
        return self._post("/v1/service/l300/l2018_live_inserttabL300_prov", param)
