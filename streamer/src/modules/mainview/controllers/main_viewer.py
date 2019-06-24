from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from src.modules.bottomleft.controllers.bottomleft import TextDialog
from src.modules.bottomleft.controllers.bottomleft import ImageDialog
from src.modules.bottomleft.controllers.bottomleft import AudioDialog
from src.modules.custom.pieplabel import PiepLabel
from src.modules.custom.piepimage import PiepImage
from src.modules.login.login import Login
from src.modules.stream.pmstream import PMStream
from src.modules.stream.mainstream import MainStream
from src.utils import helper
from kivy.lang import Builder
import sounddevice as sd
from kivy.core.window import Window
from kivy.clock import Clock
import threading
from threading import Thread, Event, ThreadError

Builder.load_file('src/modules/mainview/views/main_viewer.kv')


class MainView(Widget):
    control = ObjectProperty()
    login_popup = ObjectProperty()
    right_content = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)

    def on_start(self):
        self.init_right_content_cam()
        self.init_right_content_presenter()

    def init_right_content_cam(self):
        self.right_content.tab_camera.ls_camera.set_data()

    def init_right_content_presenter(self):
        self.right_content.tab_presenter.ls_presenter.set_data()

    def changeSrc(self, data_src):
        pass

    def openSetting(self):
        pass

    def openLogin(self):
        self.login_popup = Login(self)
        self.login_popup.open()
