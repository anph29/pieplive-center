import kivy
from kivy.config import Config
import src.utils.helper as helper
#app_width, app_height = helper._read_setting('application_resolution')
#1490 x 940
Config.set('graphics', 'width', 1492)
Config.set('graphics', 'height', 940)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '30')
Config.set('graphics', 'left', '20')
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'maxfps', '0')
Config.set('graphics', 'fbo', 'force-hardware')#one of ‘hardware’, ‘software’ or ‘force-hardware’
Config.set('graphics', 'kivy_clock', 'free_all')#one of default, interrupt, free_all, free_only
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'window_icon', 'src/icons/logo_stream.ico')

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.factory import Factory

from kivy.garden.iconfonts import iconfonts

from src.modules.mainview.main import MainView
from src.modules.rightcontentview.rightcontentstream import RightContentStream

from src.modules.custom.imagebutton import ImageButton
from src.modules.custom.popup import PiepMePopup
from src.modules.custom.pieplabel import PiepLabel
from src.modules.custom.piepimage import PiepImage
from src.modules.bufferview.buffer import Buffer
from src.modules.controlview.control import Control
from src.modules.kvcam.kivycamera import KivyCameraHeadless

from src.modules.bottomleft.bottomleft import BottomLeft

from src.modules.rightcontentview.listview import ListCamera
from src.modules.rightcontentview.gridview import GridCamera
from src.modules.rightcontentview.itemlabel import ItemLabel
from src.modules.rightcontentview.listview import ListPresenter

iconfonts.register('default_font', 'src/fonts/iconfont_sample.ttf','src/fonts/iconfont_sample.fontd')
iconfonts.register('fontawesome', 'src/fonts/fontawesome.ttf','src/fonts/fontawesome.fontd')
KIVY_FONTS = helper._load_fonts()
for font in KIVY_FONTS:
    LabelBase.register(**font)

class PiepStream(App):
    title = "Piep-Live-Center"
    mainView = ObjectProperty()

    def __init__(self, **kwargs):
        super(PiepStream, self).__init__(**kwargs)

    def build(self):
        return self.mainView

    def on_start(self):
        helper.getApRoot().on_start()

    def on_stop(self):
        helper.getApRoot().on_stop()

if __name__ == '__main__':
    PiepStream().run()
