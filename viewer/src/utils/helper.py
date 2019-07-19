import os
import re
import json
import math
import base64
from src.utils import zip_helper
import datetime
import cv2
"""
"""
_BASE_PATH              = os.path.abspath('../resource').replace('\\', '/') + '/'
_PATH_SETTING           = _BASE_PATH + 'cfg/setting.json'
_PATH_FONT              = _BASE_PATH + 'cfg/font.json'
_PATH_STORE             = _BASE_PATH + 'cfg/store.json'
_PATH_IMAGE             = _BASE_PATH + 'cfg/image.json'
_PATH_VIDEO             = _BASE_PATH + 'cfg/video.json'
_PATH_CAMERA            = _BASE_PATH + 'cfg/camera.json'
_PATH_PRESENTER         = _BASE_PATH + 'cfg/presenter.json'
_PATH_SCHEDULE          = _BASE_PATH + 'cfg/schedule.json'
_PATH_STATICSOURCE      = _BASE_PATH + 'cfg/staticsource.json'
_ICONS_PATH             = _BASE_PATH + 'icons/'
_IMAGES_PATH            = _BASE_PATH + 'images/'
_LOGO_STREAMER          = _ICONS_PATH + 'logo-streamer.ico'
_LOGO_VIEWER            = _ICONS_PATH + 'logo-viewer.png'
"""
"""
"""
ls schedule
"""     
def _load_schedule():
    return loadJSON(_PATH_SCHEDULE)

def _write_schedule(data):
    writeJSON(_PATH_SCHEDULE, data)

def _add_to_schedule(data):
    appendJSON(_PATH_SCHEDULE, data)

def calcCurentSeccondInDay():
    dt = datetime.datetime.now()
    return dt.hour * 3600 + dt.minute * 60 + dt.second

def _calc_time_point(index, schedule=[], startTime=0):
    callWrite = not bool(schedule)
    schedule = schedule or _load_schedule()
    startTime = startTime or calcCurentSeccondInDay()
    newSchedule = []
    flagStart = False
    currentPoint = startTime
    for i, sch in enumerate(schedule):
        if i == index:
            flagStart = True
        #
        if flagStart:
            sch['timepoint'] = currentPoint
            currentPoint += sch['duration']
        else:
            sch['timepoint'] = 0
        #
        newSchedule.append(sch)
    #
    if callWrite:
        _write_schedule(newSchedule)
    else:
        return newSchedule

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
ls image resource
"""
def _load_image():
    return loadJSON(_PATH_IMAGE)

def _write_image(data):
    writeJSON(_PATH_IMAGE, data)

def _add_to_image(data):
    appendJSON(_PATH_IMAGE, data)
"""
ls video resource
"""
def _load_video():
    return loadJSON(_PATH_VIDEO)

def _write_video(data):
    writeJSON(_PATH_VIDEO, data)

def _add_to_video(data):
    appendJSON(_PATH_VIDEO, data)
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
    return loadJSON(_PATH_STATICSOURCE)

def _write_lsStaticSource(data):
   writeJSON(_PATH_STATICSOURCE, data)
   
def _add_to_lsStaticSource(data):
    appendJSON(_PATH_STATICSOURCE, data)
"""
ls font
"""
def _load_font():
    return loadJSON(_PATH_FONT)

def _write_font(data):
   writeJSON(_PATH_FONT, data)
   
def _add_to_font(data):
    appendJSON(_PATH_FONT, data)
"""
setting
"""

def _read_setting(key=None):
    setting = loadJSON(_PATH_SETTING)
    return setting[key] if key is not None else setting

def _write_setting(data):
    writeJSON(_PATH_SETTING, data)
   
def _load_setting():
    return loadJSON(_PATH_SETTING)

"""
JSON helper
"""
def loadJSON(path):
    with open(path, 'r', encoding='utf-8') as jdata:
        return json.load(jdata)

def writeJSON(path, data):
     with open(path, 'w', encoding='utf-8') as jflie:
        json.dump(data, jflie, indent=2)

def appendJSON(path, data, auto_increment=False):
    jcam = loadJSON(path)
    jcam.append(data)
    writeJSON(path,jcam)

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


def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))


def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

# seconds in number -> toObj ? {h,m,s} : [hh:]mm:ss
def convertSecNoToHMS(seconds, toObj=False):
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
        return f'{hs}:{ms}:{ss}'

def convertHMSNoToSec(hms):
    h,m,s = hms.values()
    return int(s) + int(m) * 60 + int(h) * 60 ** 2

def makeSureResourceFolderExisted():
    resrcPth = '../resource'
    #
    if not os.path.exists(resrcPth):
        zip_helper.extractZip('./resource.zip', '../')
    #
    if not os.path.exists(resrcPth + '/cfg'):
        os.mkdir(resrcPth + '/cfg')
    #
    checkResourceExistAndWriteIfNot('store', data={})
    for target in ['video', 'image', 'camera', 'schedule', 'presenter', 'staticsource', 'setting', 'font']:
        checkResourceExistAndWriteIfNot(target)

def checkResourceExistAndWriteIfNot(target, data=[]):
    path = f'{_BASE_PATH}cfg/{target}.json'
    if not os.path.isfile(path):
        writeJSON(path, data)

def getMTypeFromUrl(url):
    URL = url.upper()
    if 'RTSP' in URL:
            return 'RTSP'
    elif 'MP4' in URL:
            return 'MP4'
    elif 'M3U8' in URL:
            return 'M3U8'
    elif 'JPG' in URL or 'PNG' in URL:
            return 'IMG'
    else:
            return False

def getVideoDuration(fpath):
    try:
        dura = 0
        _cap = cv2.VideoCapture(fpath)
        if _cap.isOpened():
            fps = _cap.get(cv2.CAP_PROP_FPS)
            fps = fps if fps > 25 else 25
            total = _cap.get(cv2.CAP_PROP_FRAME_COUNT)
            dura =  int(total / fps)
            
        _cap.release()
        return dura
    except expression:
        return 0
