import json
import re
import pyqrcode
import base64

__GLOBALPATH__ = "__globalpath__"
__LOCALPATH__ = "__localpath__"
LOGO = "logo"
LSCAMERA = "lscamera"
LSPRESENTER = "lspresenter"
LSSTATICSOURCE = "lsstaticsource"


def _read_setting(key=None):
    with open('src/cfg/setting.json', 'r', encoding='utf-8') as json_setting:
        setting = json.load(json_setting)
        return setting[key] if key is not None else setting


_SETTING = _read_setting()
_BASE_PATH = _SETTING[__LOCALPATH__]  # switch to local here
_LOGO_PATH = _BASE_PATH + _SETTING[LOGO]
_LSCAM_PATH = _BASE_PATH + _SETTING[LSCAMERA]
_LS_PRESENTER_PATH = _BASE_PATH + _SETTING[LSPRESENTER]
_LS_LSSTATICSOURCE_PATH = _BASE_PATH + _SETTING[LSSTATICSOURCE]


def _load_lscam():
    with open(_LSCAM_PATH, 'r', encoding='utf-8') as json_lscam:
        return json.load(json_lscam)


def _write_lscam(data):
    with open(_LSCAM_PATH, 'w', encoding='utf-8') as json_lscam:
        json.dump(data, json_lscam, indent=4)


def _add_to_lscam(data):
    with open(_LSCAM_PATH, 'r', encoding='utf-8') as rcam:
        jcam = json.load(rcam)
        jcam.append(data)
    with open(_LSCAM_PATH, 'w', encoding='utf-8') as wcam:
        json.dump(jcam, wcam, indent=4)


def _load_ls_presenter():
    with open(_LS_PRESENTER_PATH, 'r', encoding='utf-8') as json_lscam:
        return json.load(json_lscam)


def _load_lsStaticSource():
    with open(_LS_LSSTATICSOURCE_PATH, 'r',
              encoding='utf-8') as json_lscam:
        return json.load(json_lscam)


def _write_lsStaticSource(data):
    with open(_LS_LSSTATICSOURCE_PATH, 'w',
              encoding='utf-8') as json_lscam:
        json.dump(data, json_lscam, indent=4)


##################################################################s#########################################################################


def removeUnicode(str):
    str = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵÄä]", 'a', str)
    str = re.sub(r"[èéẹẻẽêềếệểễ]", 'e', str)
    str = re.sub(r"[ìíịỉĩ]", 'i', str)
    str = re.sub(r"[òóọỏõôồốộổỗơờớợởỡÖö]", 'o', str)
    str = re.sub(r"[ùúụủũưừứựửữ]", 'u', str)
    str = re.sub(r"[ỳýỵỷỹ]", 'y', str)
    str = re.sub(r"đ", "d", str)
    str = re.sub(r"[ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴ]", 'A', str)
    str = re.sub(r"[ÈÉẸẺẼÊỀẾỆỂỄ]", 'E', str)
    str = re.sub(r"[ÌÍỊỈĨ]", 'I', str)
    str = re.sub(r"[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]", 'O', str)
    str = re.sub(r"[ÙÚỤỦŨƯỪỨỰỬỮÜü]", 'U', str)
    str = re.sub(r"[ỲÝỴỶỸ]", 'Y', str)
    str = re.sub(r"Đ", 'D', str)
    return str


def removeUnicodeLowerRmvSpace(str):
    str = str.replace(r"[àáạảãâầấậẩẫăằắặẳẵÄä]", 'a', str)
    str = str.replace(r"[èéẹẻẽêềếệểễ]", 'e', str)
    str = str.replace(r"[ìíịỉĩ]", 'i', str)
    str = str.replace(r"[òóọỏõôồốộổỗơờớợởỡÖö]", 'o', str)
    str = str.replace(r"[ùúụủũưừứựửữ]", 'u', str)
    str = str.replace(r"[ỳýỵỷỹ]", 'y', str)
    str = str.replace(r"đ", "d", str)
    str = str.replace(r"[\s:\/.]", "", str)
    return str


def _load_fonts():
    with open('src/cfg/lsfont.json', 'r', encoding='utf-8') as json_lsfont:
        return json.load(json_lsfont)


def generate_qr(token, fpath):
    qr_code = pyqrcode.create(token)
    qr_code.png(fpath, scale=8)


def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))


def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
