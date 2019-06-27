import json
import re
import pyqrcode
import base64
import os
import zipfile


def _read_setting(key=None):
    with open('src/cfg/setting.json', 'r', encoding='utf-8') as json_setting:
        setting = json.load(json_setting)
        return setting[key] if key is not None else setting


__GLOBALPATH__ = "__globalpath__"
__LOCALPATH__ = "__localpath__"
_SETTING = _read_setting()
# switch to local here [__LOCALPATH__]
basePath = os.path.dirname(os.path.abspath(_SETTING[__GLOBALPATH__] + '/a'))
_BASE_PATH = basePath.replace('\\', '/') + '/'
_LOGO_PATH = _BASE_PATH + _SETTING["logo"]
_LSCAM_PATH = _BASE_PATH + _SETTING["lscamera"]
_LS_PRESENTER_PATH = _BASE_PATH + _SETTING["lspresenter"]
_LS_LSSTATICSOURCE_PATH = _BASE_PATH + _SETTING["lsstaticsource"]
_FONT_SETTING_PATH = _BASE_PATH + _SETTING["font_setting"]
_STORE_SETTING = _BASE_PATH + _SETTING["store_setting"]

###########################################################################################################################################


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


###########################################################################################################################################


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
    with open(_FONT_SETTING_PATH, 'r', encoding='utf-8') as json_lsfont:
        return json.load(json_lsfont)


def generate_qr(token, fpath):
    qr_code = pyqrcode.create(token)
    qr_code.png(fpath, scale=8)


def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))


def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
