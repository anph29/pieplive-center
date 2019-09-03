import os
import kivy
from kivy.config import Config
import src.utils.kivyhelper as kivy_helper
from src.utils import helper, zip_helper, admin
#app_width, app_height = helper._read_setting('application_resolution')
#1532 x 940
Config.set('graphics', 'width', 1752)
Config.set('graphics', 'height', 955)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', 30)
Config.set('graphics', 'left', 20)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'maxfps', 0)
# Config.set('graphics', 'fbo', 'force-hardware')#one of hardware, software or force-hardware
Config.set('graphics', 'kivy_clock', 'free_all')#one of default, interrupt, free_all, free_only
Config.set('kivy', 'window_icon', helper._LOGO_STREAMER)
Config.write()

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.factory import Factory

from src.modules.mainview import MainView

from src.modules.custom.imagebutton import ImageButton
from src.modules.custom.popup import PiepMePopup
from src.modules.custom.pieplabel import PiepLabel
from src.modules.custom.piepimage import PiepImage

from src.modules.bottomleft.bottomleft import BottomLeft

from src.modules.rightcontentview.rightcontent import RightContent
from src.modules.rightcontentview.listview import *
from src.modules.rightcontentview.gridview import GridCamera


class PiepStream(App):
    title = "PiepLiveCenter-Streamer"
    mainView = ObjectProperty()

    def __init__(self, **kwargs):
        super(PiepStream, self).__init__(**kwargs)

    def build(self):
        return self.mainView

    def on_start(self):
        kivy_helper.getApRoot().on_start()

    def on_stop(self):
        kivy_helper.getApRoot().on_stop()

if __name__ == '__main__':
    helper.makeSureResourceFolderExisted()
    KIVY_FONTS = helper._load_font()
    for font in KIVY_FONTS:
        LabelBase.register(**font)
    PiepStream().run()
