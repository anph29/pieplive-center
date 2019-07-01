import os
import re
import json
import math
import base64
import zipfile
import pyqrcode
"""
"""
_BASE_PATH              = os.path.abspath('../resource').replace('\\', '/') + '/'
_SETTING_PATH           = _BASE_PATH + 'cfg/setting.json'
_PATH_STORE             = _BASE_PATH + 'cfg/store.json'
_PATH_CUSTOM_RESOURCE   = _BASE_PATH + 'cfg/custom_resource.json'
_PATH_CAMERA            = _BASE_PATH + 'cfg/camera.json'
_PATH_PRESENTER         = _BASE_PATH + 'cfg/presenter.json'
_PATH_SCHEDULE          = _BASE_PATH + 'cfg/schedule.json'
_PATH_STATICSOURCE      = _BASE_PATH + 'cfg/staticsource.json'
_ICONS_PATH             = _BASE_PATH + 'icons/'
_LOGO_STREAMER          = _ICONS_PATH + 'logo-streamer.ico'
_LOGO_VIEWER            = _ICONS_PATH + 'logo-viewer.png'
"""
"""

"""
ls camera
"""
def _load_lscam():
    return loadJSON(_PATH_CAMERA)

def _write_lscam(data):
    writeJSON(_PATH_CAMERA, data)

def _add_to_lscam(data):
    appendJSON(_PATH_CAMERA, data)
"""
ls custom resource
"""
def _load_custom_resource():
    loadJSON(_PATH_CUSTOM_RESOURCE)

def _write_custom_resource(data):
    writeJSON(_PATH_CUSTOM_RESOURCE, data)

def _add_to_custom_resource(data):
    appendJSON(_PATH_CUSTOM_RESOURCE, data)
"""
ls presenter
"""
def _load_ls_presenter():
    return loadJSON(_PATH_PRESENTER)

def _write_lspresenter(data):
    writeJSON(_PATH_PRESENTER, data)

def _add_to_spresenter(data):
    appendJSON(_PATH_PRESENTER, data)
"""
ls static source
"""
def _load_lsStaticSource():
    loadJSON(_PATH_STATICSOURCE)

def _write_lsStaticSource(data):
   writeJSON(_PATH_STATICSOURCE, data)
   
def _add_to_lsStaticSource(data):
    appendJSON(_PATH_STATICSOURCE, data)
"""
setting
"""

def _read_global_setting(key=None):
    with open(_SETTING_PATH, 'r', encoding='utf-8') as json_setting:
        setting = json.load(json_setting)
        return setting[key] if key is not None else setting

def _read_setting(key=None):
    with open('src/cfg/setting.json', 'r', encoding='utf-8') as json_setting:
        setting = json.load(json_setting)
        return setting[key] if key is not None else setting

"""
"""

def loadJSON(path):
    with open(path, 'r', encoding='utf-8') as jdata:
        return json.load(jdata)

def writeJSON(path, data):
     with open(path, 'w', encoding='utf-8') as jdata:
        json.dump(data, jdata, indent=2)

def appendJSON(path, data, auto_increment=False):
    jcam = loadJSON(path)
    jcam.append(data)
    writeJSON(path,data)

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

# seconds in number -> toObj ? {h,m,s} : [hh:]mm:ss
def convertSecNoToHMS(seconds, toObj=False) :
    seconds = math.floor(seconds)
    h = math.floor(seconds / 3600)
    m = math.floor((seconds % 3600) / 60)
    s = seconds - h * 3600 - m * 60
    hs = ('','0')[h < 10] + str(h)
    ms = ('','0')[m < 10] + str(m)
    ss = ('','0')[s < 10] + str(s)
    if toObj:
        return { 'h': hs, 'm': ms, 's': ss } 
    else:
        return (('', hs + ':')[h>0]) + ms + ':' + ss

