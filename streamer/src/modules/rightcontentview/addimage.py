from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from src.modules.custom.filechoose import FileChooser
from src.utils import ftype, helper
import src.utils.kivyhelper as kv_helper

Builder.load_file('src/ui/addimage.kv')

class AddImage(Popup):
    name = ObjectProperty()
    url = ObjectProperty()
    error = BooleanProperty(False)
    resource_type = ''
    use_local = False

    def __init__(self, parent):
        super(AddImage, self).__init__()

    def add_to_lsimage(self):
        helper._add_to_image({
            "name": self.name.text,
            "url": self.url.text,
            "type": "IMG"
        })
        kv_helper.getApRoot().init_right_content_image()
        self.dismiss()

    def on_ok(self):
        if self.use_local:
            self.add_to_lsimage()
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
            else:
                self.error = True

    def local_file(self, fpath, ftype):
        self.use_local = True
        self.resource_type = ftype
        self.url.text = fpath.replace('\\', '/')

    def get_type_from_link(self):
        URL = self.url.text.upper()
        if '.JPG' in URL or '.PNG' in URL or '.GIF' in URL or '.JPGE' in URL or '.JPX' in URL or '.WEBP' in URL or '.CR2' in URL or '.TIF' in URL or '.BMP' in URL or '.JXR' in URL or '.ICO' in URL:
            return 'IMG'
        else:
            return False
