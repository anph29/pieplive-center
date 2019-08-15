from urllib.request import Request, urlopen
from urllib.request import HTTPError
from urllib import parse
import json
import sys
from src.utils import scryto
from collections import OrderedDict
import requests

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

    def querystring(self, param):
        """ mk query string for GET method """
        sorted_key = sorted(param)
        maped_ls = map(lambda v: f"{v}={parse.quote(str(param[v]))}", sorted_key)
        return "&".join(list(maped_ls))

    """-------------------------------------------------------------------------------------------------------------------------
                                                    no
    -------------------------------------------------------------------------------------------------------------------------"""
    
    def _get_static(self, path):
        return self.http_request_static(path, 'GET')

    """-------------------------------------------------------------------------------------------------------------------------
                                                    HTTP_REQUEST
    -------------------------------------------------------------------------------------------------------------------------"""

    def http_request(self, path, param, method, tokenMethod=scryto.createTokenV3):
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
        payload = json.dumps(param)
        headers = {"Content-Type": "application/json", "cache-control": "no-cache"}
        # 7. mk request
        print(f">> {method} {url} data={payload}")
        response = requests.request(method, url, data=payload, headers=headers)
        # 8. receive RESPONSE
        json_str = response.text
        data_json = json.loads(json_str)
        print(
            f'>> RESPONSE -> status={data_json["status"]}, len={len(json_str)}'
        )
        return data_json

    """-------------------------------------------------------------------------------------------------------------------------
                                                    HTTP_REQUEST
    -------------------------------------------------------------------------------------------------------------------------"""

    def http_request_(self, path, param, method, tokenMethod=scryto.createTokenV3):
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
        data = self.uber_urlencode({} if method is "GET" else param).encode("utf-8")
        # 7. mk request
        req = Request(url, data=data, method=method)
        req.add_header("Accept", "application/json")
        print(f">> {method} {url} data={data}")
        # 8. receive RESPONSE
        try:
            with urlopen(req) as response:
                json_str = response.read().decode("utf-8")
                data_json = json.loads(json_str)
                print(
                    f'>> RESPONSE -> status={data_json["status"]}, len={len(json_str)}'
                )
                return data_json
        except HTTPError as e:
            print("http_request error", e, e.code)

        """-------------------------------------------------------------------------------------------------------------------------
                                                        HTTP_REQUEST_STATIC
        -------------------------------------------------------------------------------------------------------------------------"""

    def http_request_static(self, path, method):
        """ ROOT request method """
        # 1. calc url from path
        url = path
        # 6. calc post data
        data = parse.urlencode({}).encode("utf-8")
        # 7. mk request
        req = Request(url, data=data, method=method)
        req.add_header("Accept", "application/json")
        # 8. receive RESPONSE
        try:
            with urlopen(req) as response:
                json_str = response.read().decode("utf-8")
                # data_json = json.loads(json_str)
                return json_str
        except Exception as e:
            print("Exception:", e)
            return None

    """-------------------------------------------------------------------------------------------------------------------------
                                                        UBER URL ENCODE
    -------------------------------------------------------------------------------------------------------------------------"""

    def uber_urlencode(self, params):
        """Urlencode a multidimensional dict."""

        # Not doing duck typing here. Will make debugging easier.
        if not isinstance(params, dict):
            raise TypeError("Only dicts are supported.")

        params = self.flatten(params)
        url_params = OrderedDict()
        for param in params:
            value = param.pop()
            name = self.parametrize(param)
            if isinstance(value, (list, tuple)):
                name += "[]"
            url_params[name] = value
        return parse.urlencode(url_params, doseq=True)

    def flatten(self, d):
        """Return a dict as a list of lists.
        >>> flatten({"a": "b"})
        [['a', 'b']]
        >>> flatten({"a": [1, 2, 3]})
        [['a', [1, 2, 3]]]
        >>> flatten({"a": {"b": "c"}})
        [['a', 'b', 'c']]
        >>> flatten({"a": {"b": {"c": "e"}}})
        [['a', 'b', 'c', 'e']]
        >>> flatten({"a": {"b": "c", "d": "e"}})
        [['a', 'b', 'c'], ['a', 'd', 'e']]
        >>> flatten({"a": {"b": "c", "d": "e"}, "b": {"c": "d"}})
        [['a', 'b', 'c'], ['a', 'd', 'e'], ['b', 'c', 'd']]
        """

        if not isinstance(d, dict):
            return [[d]]
        returned = []
        for key, value in sorted(d.items()):
            # Each key, value is treated as a row.
            nested = self.flatten(value)
            for nest in nested:
                current_row = [key]
                current_row.extend(nest)
                returned.append(current_row)
        return returned

    def parametrize(self, params):
        """Return list of params as params.
        >>> parametrize(['a'])
        'a'
        >>> parametrize(['a', 'b'])
        'a[b]'
        >>> parametrize(['a', 'b', 'c'])
        'a[b][c]'
        """
        returned = str(params[0])
        returned += "".join("[" + str(p) + "]" for p in params[1:])
        return returned
