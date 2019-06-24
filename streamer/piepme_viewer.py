import kivy
from kivy.config import Config
from src.utils import helper
app_width, app_height = helper._read_setting('application_resolution')
Config.set('graphics', 'width', app_width)
Config.set('graphics', 'height', app_height)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '30')
Config.set('graphics', 'left', '20')
Config.set('graphics', 'maxfps', '0')

from src.modules.rightcontentview.controllers.listview import ListPresenter
from src.modules.rightcontentview.controllers.itemcameraviewer import ItemCameraViewer
from src.modules.rightcontentview.controllers.gridview import GridCamera
from src.modules.rightcontentview.controllers.listview import ListCamera
from src.modules.rightcontentview.controllers.rightcontentviewer import RightContentViewer
from src.modules.kvcam.kivycamera import KivyCameraLow
from src.modules.bottomleft.controllers.bottomleft import BottomLeft
from src.modules.controlview.controlviewer import ControlViewer
from src.modules.bufferview.buffer import Buffer
from src.modules.custom.piepimage import PiepImage
from src.modules.custom.pieplabel import PiepLabel
from src.modules.custom.popup import PiepMePopup
from src.modules.custom.imagebutton import ImageButton
from src.modules.stream.pmstream import PMStream
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
import cv2
from kivy.garden.iconfonts import iconfonts
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from src.modules.mainview.controllers.main_viewer import MainView
from kivy.app import App
# Config.set('graphics', 'fbo', 'force-hardware')#one of ‘hardware’, ‘software’ or ‘force-hardware’
# one of default, interrupt, free_all, free_only
Config.set('graphics', 'kivy_clock', 'free_only')
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'window_icon', 'src/images/logo.png')


kivy.require('1.10.1')
# init fonts
# iconfonts.create_fontdict_file('fontawesome.css', 'fontawesome.fontd')
iconfonts.register('default_font', 'src/fonts/iconfont_sample.ttf',
                   'src/fonts/iconfont_sample.fontd')
iconfonts.register('fontawesome', 'src/fonts/fontawesome.ttf',
                   'src/fonts/fontawesome.fontd')
KIVY_FONTS = helper._load_fonts()
for font in KIVY_FONTS:
    LabelBase.register(**font)


# class Splash(Screen):
#     def skip(self, dt):
#         self.manager.current = "MainScreen"

#     def on_enter(self, *args):
#         Clock.schedule_once(self.skip, 5)


# class MainScreen(Screen):
#     pass


# class PiepMeViewer(ScreenManager):
#     pass


class PiepMe(App):
    title = "PiepMe Live Center"
    mainView = ObjectProperty()

    def build(self):
        return self.mainView

    def on_start(self):
        helper.getApRoot().on_start()

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        # helper.getApRoot().on_stop()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    PiepMe().run()
