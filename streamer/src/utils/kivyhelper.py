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

def _load_fonts():
    with open('src/cfg/lsfont.json', 'r', encoding='utf-8') as json_lsfont:
        return json.load(json_lsfont)

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