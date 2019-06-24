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
#Config.set('graphics', 'fbo', 'force-hardware')#one of ‘hardware’, ‘software’ or ‘force-hardware’
Config.set('graphics', 'kivy_clock', 'free_only')#one of default, interrupt, free_all, free_only
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'window_icon', 'src/images/logo.png')


from kivy.app import App
from src.modules.mainview.controllers.main import MainView
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase
from kivy.garden.iconfonts import iconfonts
import cv2

kivy.require('1.10.1')

stream_domain = 'rtmp://livevn.piepme.com/cam/'
#stream_key = '7421.bf586e24e22cfc1a058ba9e8cf96afee?token=bf586e24e22cfc1a058ba9e8cf96afee&SRC=WEB&FO100=7421&PL300=7940&LN301=180&LV302=115.73.208.139&LV303=0982231325&LL348=1554461547035&UUID=247cbf2ee3f0bda1&NV124=vn&PN303=15&POS=1'
# https://livevn.piepme.com/camhls/7421.bf586e24e22cfc1a058ba9e8cf96afee.m3u8
stream_key = '7421.b99e3cde588f1a8a25c0f002050f0893?token=b99e3cde588f1a8a25c0f002050f0893&SRC=WEB&FO100=7421&PL300=7939&LN301=180&LV302=115.73.208.139&LV303=0982231325&LL348=1554458516364&UUID=247cbf2ee3f0bda1&NV124=vn&PN303=15&POS=0'
# https://livevn.piepme.com/camhls/7421.b99e3cde588f1a8a25c0f002050f0893.m3u8

#init fonts
#iconfonts.create_fontdict_file('fontawesome.css', 'fontawesome.fontd')
iconfonts.register('default_font', 'src/fonts/iconfont_sample.ttf',
                   'src/fonts/iconfont_sample.fontd')
iconfonts.register('fontawesome', 'src/fonts/fontawesome.ttf',
                   'src/fonts/fontawesome.fontd')
KIVY_FONTS = helper._load_fonts()
for font in KIVY_FONTS:
    LabelBase.register(**font)


class PiepMe(App):
    title = "PiepMe Live Center"
    mainView = ObjectProperty()

    def build(self):
        return self.mainView

    def on_start(self):
        helper.getApRoot().on_start()

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        helper.getApRoot().on_stop()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    PiepMe().run()