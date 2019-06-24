from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from src.modules.custom.filechoose import FileChooser
from src.utils import ftype, helper

Builder.load_file('src/ui/addcamera.kv')


class AddCamera(Popup):
    name = ObjectProperty()
    url = ObjectProperty()
    error = BooleanProperty(False)
    resource_type = ''
    use_local = False

    def __init__(self, parent):
        super(AddCamera, self).__init__()

    def add_to_lscam(self):
        helper._add_to_lscam({
            "name": self.name.text,
            "url": self.url.text,
            "type": self.resource_type
        })
        helper.getApRoot().init_right_content_cam()
        self.dismiss()

    def on_ok(self):
        if self.use_local:#
            self.add_to_lscam()
        elif len(self.name.text) > 0:#
            resource_type = self.get_type_from_link()
            if resource_type:
                self.add_to_lscam()
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
        elif 'MP4' in URL:
            return 'MP4'
        elif 'M3U8' in URL:
            return 'M3U8'
        else:
            return False
