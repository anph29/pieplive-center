import os
import re
import json
import math
import base64
from . import zip_helper
import datetime
import cv2
import shutil
"""
VARIABLE
"""
USER_LOCAL_PATH = os.environ['LOCALAPPDATA'].replace('\\', '/')
_BASE_PATH = USER_LOCAL_PATH + '/PiepLiveCenter/'
_PATH_FONT = f'{_BASE_PATH}cfg/font.json'
_PATH_STORE = f'{_BASE_PATH}cfg/store.json'
_PATH_IMAGE = f'{_BASE_PATH}cfg/image.json'
_PATH_VIDEO = f'{_BASE_PATH}cfg/video.json'
_PATH_AUDIO = f'{_BASE_PATH}cfg/audio.json'
_PATH_CAMERA = f'{_BASE_PATH}cfg/camera.json'
_PATH_SCHEDULE = f'{_BASE_PATH}cfg/schedule.json'
_PATH_SETTING = f'{_BASE_PATH}cfg/setting.json'
_PATH_PRESENTER = f'{_BASE_PATH}cfg/presenter.json'
_PATH_KEY_STREAM = f'{_BASE_PATH}cfg/keystream.json'
_PATH_SCHEDULE_DIR = f'{_BASE_PATH}cfg/schedules/'
_PATH_STATICSOURCE = f'{_BASE_PATH}cfg/staticsource.json'
_PATH_SCHEDULE_SORTED = f'{_BASE_PATH}cfg/schedules/sorted.json'
_ICONS_PATH = f'{_BASE_PATH}icons/'
_IMAGES_PATH = f'{_BASE_PATH}images/'
_LOGO_STREAMER = f'{_ICONS_PATH}logo-streamer.ico'
_LOGO_VIEWER = f'{_ICONS_PATH}logo-viewer.png'

"""
schedule
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


def calc_schedule_runtime(index, schedule=[], startTime=0):
    isWriteToFile = not bool(schedule)
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
    if isWriteToFile:
        _write_schedule(newSchedule)
    else:
        return newSchedule


"""
multi schedule
"""


def _load_sorted_schedule():
    return loadJSON(_PATH_SCHEDULE_SORTED)


def _write_sorted_schedule(data):
    writeJSON(_PATH_SCHEDULE_SORTED, data)


def _add_to_sorted_schedule(data):
    appendJSON(_PATH_SCHEDULE_SORTED, data)


def list_all_schedule():
    dirs = os.listdir(_PATH_SCHEDULE_DIR)
    return list(map(lambda f: f.endswith(".json"), dirs))


def new_schedule_container(fname, data=[]):
    path = get_verified_fname(fname)
    path = makeSureScheduleFile(fname)
    if os.path.isfile(path):
        return False  # failed to create
    else:
        writeJSON(path, data)
        return True


def delete_schedule_container(fname):
    path = makeSureScheduleFile(fname)
    if os.path.isfile(path):
        os.remove(path)


def duplicate_schedule_container(frName, toName):
    src = makeSureScheduleFile(frName)
    dst = makeSureScheduleFile(toName)
    shutil.copyfile(src, dst)
    return toName

# -- @@ -- @@ --


def _load_schedule_width_fname(fname):
    path = makeSureScheduleFile(fname)
    if os.path.isfile(path):
        return loadJSON(path)


def _write_schedule_width_fname(fname, data):
    path = makeSureScheduleFile(fname)
    if os.path.isfile(path):
        writeJSON(path, data)


def _add_to_schedule_width_fname(fname, data):
    path = makeSureScheduleFile(fname)
    if os.path.isfile(path):
        appendJSON(path, data)


def get_verified_fname(fname):
    fname = removeUnicode(fname)
    return re.sub(r"[^a-zA-Z0-9\.-_]", '', fname)


def makeSureScheduleFile(name):
    fname = name if name.endswith('.json') else name + '.json'
    return f'{_PATH_SCHEDULE_DIR}{fname}'


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


def _add_to_lspresenter(data):
    appendJSON(_PATH_PRESENTER, data)


"""
ls audio
"""


def _load_ls_audio():
    return loadJSON(_PATH_AUDIO)


def _write_lsaudio(data):
    writeJSON(_PATH_AUDIO, data)


def _add_to_lsaudio(data):
    appendJSON(_PATH_AUDIO, data)


"""
ls key stream
"""


def _load_ls_key():
    return loadJSON(_PATH_KEY_STREAM)


def _write_lskey(data):
    writeJSON(_PATH_KEY_STREAM, data)


def _add_to_lskey(data):
    appendJSON(_PATH_KEY_STREAM, data)


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
    writeJSON(path, jcam)


"""
UNICODE helper
"""


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


def convertSecNoToHMS(seconds, toObj=False):
    # seconds in number -> toObj ? {h,m,s} : [hh:]mm:ss
    seconds = math.floor(seconds)
    h = math.floor(seconds / 3600)
    m = math.floor((seconds % 3600) / 60)
    s = seconds - h * 3600 - m * 60
    hs = ('', '0')[h < 10] + str(h)
    ms = ('', '0')[m < 10] + str(m)
    ss = ('', '0')[s < 10] + str(s)
    if toObj:
        return {'h': hs, 'm': ms, 's': ss}
    else:
        return f'{hs}:{ms}:{ss}'


def convertHMSNoToSec(hms):
    h, m, s = hms.values()
    return int(s) + int(m) * 60 + int(h) * 60 ** 2


def makeSureResourceFolderExisted():
     # resource
    if not os.path.exists(_BASE_PATH):
        zip_helper.extractZip('./PiepLiveCenter.zip', USER_LOCAL_PATH)
    # resource/temp
    if not os.path.exists(f'{_BASE_PATH}temp'):
        os.mkdir(f'{_BASE_PATH}temp')
    # resource/cfg
    if not os.path.exists(f'{_BASE_PATH}cfg'):
        os.mkdir(f'{_BASE_PATH}cfg')
    # resource/cfg/schedules
    if not os.path.exists(f'{_BASE_PATH}cfg/schedules'):
        os.mkdir(f'{_BASE_PATH}cfg/schedules')
    # sorted schedule file
    if not os.path.isfile(f'{_BASE_PATH}cfg/schedules/sorted.json'):
        writeJSON(f'{_BASE_PATH}cfg/schedules/sorted.json', [])
    # store
    checkResourceExistAndWriteIfNot('store', data={})
    # setting
    checkResourceExistAndWriteIfNot('setting', data=getSettingJSONContent())
    # font
    checkResourceExistAndWriteIfNot('font', data=getFontJSONContent())
    # ...rest cfg file
    for target in ['video', 'image', 'camera', 'schedule', 'audio', 'presenter', 'staticsource', 'keystream']:
        checkResourceExistAndWriteIfNot(target)


def checkResourceExistAndWriteIfNot(target, data=[]):
    path = f'{_BASE_PATH}cfg/{target}.json'
    if not os.path.isfile(path):
        writeJSON(path, data)


def getFontJSONContent():
    return [
        {
            "name": "opensans",
            "fn_regular": f"{_BASE_PATH}fonts/opensans.ttf",
            "fn_bold": f"{_BASE_PATH}fonts/opensans-bold.ttf"
        },
        {
            "name": "roboto",
            "fn_regular": f"{_BASE_PATH}fonts/roboto.ttf"
        },
        {
            "name": "awkward-alone",
            "fn_regular": f"{_BASE_PATH}fonts/awkward-alone.ttf"
        },
        {
            "name": "good-brush",
            "fn_regular": f"{_BASE_PATH}fonts/good-brush.ttf"
        }
    ]


def getSettingJSONContent():
    return {
        "application_resolution": ["1600", "900"],
        "ouput_resolution": [1280, 720],
        "vbitrate": "4M",
        "stream_server": "",
        "stream_key": ""
    }


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
            dura = int(total / fps)
        _cap.release()
        return dura
    except expression:
        return 0
