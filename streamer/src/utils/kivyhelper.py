import json
from kivy.app import App
from src.modules.custom.popup import PiepMeConfirmPopupContent
from kivy.uix.popup import Popup
import re
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