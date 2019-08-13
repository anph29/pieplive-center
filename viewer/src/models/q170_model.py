from . import HTTP_MODEL


class Q170_model(HTTP_MODEL):
    def __init__(self):
        super(Q170_model, self).__init__()

    # GET
    # check list has role camera
    #  {
    #      FO100 user
    #      FQ180 roles
    #  }
    #
    def getListProviderWithRole(self, param):
        return self._get("/v1/service/q170/q2019_getListProviderWithRole", param)
