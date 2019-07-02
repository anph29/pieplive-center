from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from src.modules.custom.filechoose import FileChooser
from src.utils import ftype, helper
import src.utils.kivyhelper as kv_helper

Builder.load_file('src/ui/addmedia.kv')

class AddMedia(Popup):
    name = ObjectProperty()
    url = ObjectProperty()
    error = BooleanProperty(False)
    resource_type = ''
    use_local = False

    def __init__(self, parent):
        super(AddMedia, self).__init__()

    def add_to_lsmedia(self):
        helper._add_to_custom_resource({
            "name": self.name.text,
            "url": self.url.text,
            "type": self.resource_type
        })
        kv_helper.getApRoot().init_right_content_media()
        self.dismiss()

    def on_ok(self):
        if self.use_local:
            self.add_to_lsmedia()
        elif len(self.url.text) > 0:
            self.resource_type = self.get_type_from_link()
            if self.resource_type:
                self.add_to_lsmedia()
            else:
                self.error = True
        else:
            self.error = True

    def on_cancel(self):
        self.dismiss()

    def open_file_browser(self):
        self.file_browser = FileChooser(self, self.choosed_file)
        self.file_browser.open()
        self.error = False

    def choosed_file(self, selection):
        if len(selection) == 1:
            if ftype.isImage(selection[0]):
                self.local_file(selection[0], 'IMG')
            elif ftype.isVideo(selection[0]):
                self.local_file(selection[0], 'VIDEO')
            else:
                self.error = True

    def local_file(self, fpath, ftype):
        self.use_local = True
        self.resource_type = ftype
        self.url.text = fpath.replace('\\', '/')

    def get_type_from_link(self):
        URL = self.url.text.upper()
        if 'RTSP' in URL:
            return 'RTSP'
        elif '.MP4' in URL or '.AVI' in URL:
            return 'VIDEO'
        elif '.M3U8' in URL:
            return 'M3U8'
        elif '.JPG' in URL or '.PNG' in URL or '.GIF' in URL or '.JPGE' in URL:
            return 'IMG'
        else:
            return False
