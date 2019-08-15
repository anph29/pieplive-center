from urllib.request import Request, urlopen
from urllib.error import HTTPError
try:
    req = Request("https://livevn.piepme.com/hls/1932.6d94f6c1c92983cf5faabfdd848d01bf/index.m3u8", method="GET")
    with urlopen(req) as response:
        # update
        pass
except HTTPError as e:
    if e.code == 404:
        # de quy
    else:
        print (e)