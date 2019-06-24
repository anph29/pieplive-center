import kivy
from kivy.config import Config
from src.utils import helper
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
Config.set('kivy', 'window_icon', 'src/images/logo.png')

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from src.modules.mainview.controllers.main_stream import MainView
from src.modules.rightcontentview.controllers.rightcontentstream import RightContentStream
from kivy.garden.iconfonts import iconfonts

iconfonts.register('default_font', 'src/fonts/iconfont_sample.ttf',
                   'src/fonts/iconfont_sample.fontd')
iconfonts.register('fontawesome', 'src/fonts/fontawesome.ttf',
                   'src/fonts/fontawesome.fontd')
KIVY_FONTS = helper._load_fonts()
for font in KIVY_FONTS:
    LabelBase.register(**font)

class PiepLiveCenter(App):
    title = "Piep-Live-Center"
    mainView = ObjectProperty()

    def __init__(self, **kwargs):
        super(PiepLiveCenter, self).__init__(**kwargs)

    def build(self):
        return self.mainView

    def on_start(self):
        helper.getApRoot().on_start()

    def on_stop(self):
        helper.getApRoot().on_stop()

if __name__ == '__main__':
    PiepLiveCenter().run()
