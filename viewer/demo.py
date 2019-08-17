import sys
import hashlib
import re
import time


def hash_md5(s):
    s = s.encode("utf-8")
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def createTokenV3(input, isRecursive=False):
    try:
        if "token" in input:
            del input["token"]

        if isRecursive is False:
            input["v"] = "v1"
            input["keyToken"] = "Piepme2017"

        ư

        # improve non-charater from v2
        maped_ls = map(
            lambda v: (
                f"{v}=[{createTokenV3(input[v], True)}]"
                if type(input[v]) in [dict, list]
                else f"{v}={re.sub(r'[^a-zA-Z0-9]', '', str(input[v]))}"
            ),
            sorted_key,
        )
        paramStr = "&".join(list(maped_ls))
        if not isRecursive:
            print(paramStr)
        return paramStr if isRecursive else hash_md5(paramStr)
    except:
        print(sys.exc_info())


if __name__ == "__main__":
    createTokenV3(
        {
            "FO100": 1932,
            "PP300": 6660,
            "FT300": 1,
            "PO322": {
                "image": [
                    {
                        "SIZE": 0,
                        "EX": "png",
                        "fileName": "piep-ttfIu9Zt15659270199131565927019913.png",
                        "DES": "",
                        "RATIO": 1,
                        "THUMB": "https://media.cdnedge.bluemix.net/1932/images/piep-ttfIu9Zt15659270199131565927019913.png",
                        "IMG": "https://media.cdnedge.bluemix.net/1932/images/piep-ttfIu9Zt15659270199131565927019913.png",
                        "FM600": 3503,
                        "FO100": 1932,
                    }
                ],
                "live": {
                    "time": "2019-08-16T03:45:00.000Z",
                    "description": "",
                    "title": "thong test live",
                    "FL300": 8990,
                    "src": "https://livevn.piepme.com/hls/1932.fc9feb122c5467ed44796610e6bf93b9/index.m3u8",
                    "NV124": "vn",
                },
            },
        }
    )

