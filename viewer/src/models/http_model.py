from urllib.request import Request, urlopen
from urllib.request import HTTPError
from urllib import parse
import json
import sys
from src.utils import scryto


"""-------------------------------------------------------------------------------------------------------------------------
                                                        HTTP MODEL
-------------------------------------------------------------------------------------------------------------------------"""


class HTTP_MODEL:
    def __init__(self):
        self.PIEPME_HOST = "https://webservice.piepme.com"

    """-------------------------------------------------------------------------------------------------------------------------
                                                    createToken
    -------------------------------------------------------------------------------------------------------------------------"""

    def _get(self, path, param):
        return self.http_request(path, param, "GET", tokenMethod=scryto.createToken)

    def _post(self, path, param):
        return self.http_request(path, param, "POST", tokenMethod=scryto.createToken)

    def _put(self, path, param):
        return self.http_request(path, param, "PUT", tokenMethod=scryto.createToken)

    def _delete(self, path, param):
        return self.http_request(path, param, "DELETE", tokenMethod=scryto.createToken)

    def _patch(self, path, param):
        return self.http_request(path, param, "PATCH", tokenMethod=scryto.createToken)

    """-------------------------------------------------------------------------------------------------------------------------
                                                    createTokenV2
    -------------------------------------------------------------------------------------------------------------------------"""

    def v2_get(self, path, param):
        return self.http_request(path, param, "GET", tokenMethod=scryto.createTokenV2)

    def v2_post(self, path, param):
        return self.http_request(path, param, "POST", tokenMethod=scryto.createTokenV2)

    def v2_put(self, path, param):
        return self.http_request(path, param, "PUT", tokenMethod=scryto.createTokenV2)

    def v2_delete(self, path, param):
        return self.http_request(
            path, param, "DELETE", tokenMethod=scryto.createTokenV2
        )

    def v2_patch(self, path, param):
        return self.http_request(path, param, "PATCH", tokenMethod=scryto.createTokenV2)

    """-------------------------------------------------------------------------------------------------------------------------
                                                    createTokenV3
    -------------------------------------------------------------------------------------------------------------------------"""

    def v3_get(self, path, param):
        return self.http_request(path, param, "GET")

    def v3_post(self, path, param):
        return self.http_request(path, param, "POST")

    def v3_put(self, path, param):
        return self.http_request(path, param, "PUT")

    def v3_delete(self, path, param):
        return self.http_request(path, param, "DELETE")

    def v3_patch(self, path, param):
        return self.http_request(path, param, "PATCH")

    """-------------------------------------------------------------------------------------------------------------------------
                                                    HTTP_REQUEST
    -------------------------------------------------------------------------------------------------------------------------"""

    def querystring(self, param):
        """ mk query string for GET method """
        sorted_key = sorted(param)
        maped_ls = map(lambda v: f"{v}={parse.quote(str(param[v]))}", sorted_key)
        return "&".join(list(maped_ls))

    def http_request(self, path, param, method, tokenMethod=scryto.createTokenV3):
        """ ROOT request method """
        # 1. calc url from path
        url = self.PIEPME_HOST + path
        # 2. add some param
        param["SRC"] = param["SRC"] if "SRC" in param else "PiepLiveCenter"
        # 3. add token
        param["token"] = tokenMethod(param)
        # 4. del secret param
        del param["keyToken"]
        del param["v"]
        # 5. buid query string
        if method is "GET":
            url += "?" + self.querystring(param)
        # 6. calc post data
        data = parse.urlencode({} if method is "GET" else param).encode("utf-8")
        # 7. mk request
        req = Request(url, data=data, method=method)
        req.add_header("Accept", "application/json")
        print(f">>>>>>>>>> {method} {url} data={data}")
        # 8. receive RESPONSE
        try:
            with urlopen(req) as response:
                json_str = response.read().decode("utf-8")
                data_json = json.loads(json_str)
                print(
                    f'>>>>>>>>>> RESPONSE -> status={data_json["status"]}, len={len(json_str)}'
                )
                return data_json
        except HTTPError as e:
            print("http_request error", e, e.code)

