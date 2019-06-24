import json
from kivy.app import App
from src.modules.custom.popup import PiepMeConfirmPopupContent
from kivy.uix.popup import Popup
import re
import pyqrcode
import base64


def getApRoot():
    app = App.get_running_app()
    return app.root


def getAppType():
    root = getApRoot()
    if bool(root):
        if bool(root.right_content):
            return root.right_content.app_type

    return ''


def isAppViewer():
    return getAppType() == 'VIEWER'


def isAppStream():
    return getAppType() == 'STREAM'


def isAppMain():
    return getAppType() == 'MAIN'


def _load_lscam():
    with open('src/cfg/lscam.json', 'r', encoding='utf-8') as json_lscam:
        return json.load(json_lscam)


def _write_lscam(data):
    with open('src/cfg/lscam.json', 'w', encoding='utf-8') as json_lscam:
        json.dump(data, json_lscam, indent=4)


def _add_to_lscam(data):
    with open('src/cfg/lscam.json', 'r', encoding='utf-8') as rcam:
        jcam = json.load(rcam)
        jcam.append(data)
    with open('src/cfg/lscam.json', 'w', encoding='utf-8') as wcam:
        json.dump(jcam, wcam, indent=4)


def _load_ls_presenter():
    with open('src/cfg/lspresenter.json', 'r', encoding='utf-8') as json_lscam:
        return json.load(json_lscam)


def _load_lsStaticSource():
    with open('src/cfg/lsstaticsource.json', 'r',
              encoding='utf-8') as json_lscam:
        return json.load(json_lscam)


def _write_lsStaticSource(data):
    with open('src/cfg/lsstaticsource.json', 'w',
              encoding='utf-8') as json_lscam:
        json.dump(data, json_lscam, indent=4)


def _read_setting(key=None):
    with open('src/cfg/setting.json', 'r', encoding='utf-8') as json_setting:
        setting = json.load(json_setting)
        return setting[key] if key is not None else setting


"""###################################################################################################
# """


def removeUnicode(str):
    str = re.sub("[àáạảãâầấậẩẫăằắặẳẵÄä]", 'a', str)
    str = re.sub("[èéẹẻẽêềếệểễ]", 'e', str)
    str = re.sub("[ìíịỉĩ]", 'i', str)
    str = re.sub("[òóọỏõôồốộổỗơờớợởỡÖö]", 'o', str)
    str = re.sub("[ùúụủũưừứựửữ]", 'u', str)
    str = re.sub("[ỳýỵỷỹ]", 'y', str)
    str = re.sub("đ", "d", str)
    str = re.sub("[ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴ]", 'A', str)
    str = re.sub("[ÈÉẸẺẼÊỀẾỆỂỄ]", 'E', str)
    str = re.sub("[ÌÍỊỈĨ]", 'I', str)
    str = re.sub("[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]", 'O', str)
    str = re.sub("[ÙÚỤỦŨƯỪỨỰỬỮÜü]", 'U', str)
    str = re.sub("[ỲÝỴỶỸ]", 'Y', str)
    str = re.sub("Đ", 'D', str)
    return str


def removeUnicodeLowerRmvSpace(str):
    str = re.replace("[àáạảãâầấậẩẫăằắặẳẵÄä]", 'a', str)
    str = re.replace("[èéẹẻẽêềếệểễ]", 'e', str)
    str = re.replace("[ìíịỉĩ]", 'i', str)
    str = re.replace("[òóọỏõôồốộổỗơờớợởỡÖö]", 'o', str)
    str = re.replace("[ùúụủũưừứựửữ]", 'u', str)
    str = re.replace("[ỳýỵỷỹ]", 'y', str)
    str = re.replace("đ", "d", str)
    str = re.replace("[\s:\/.]", "", str)
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
