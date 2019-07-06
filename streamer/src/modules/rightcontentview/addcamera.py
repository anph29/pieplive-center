from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from src.modules.custom.filechoose import FileChooser
from src.utils import ftype, helper, scryto
import src.utils.kivyhelper as kv_helper

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
            "id":scryto.hash_md5_with_time(self.url.text.replace('\\', '/')),
            "name": self.name.text,
            "url": self.url.text.replace('\\', '/'),
            "type": 'RTSP'
        })
        kv_helper.getApRoot().init_right_content_cam()
        self.dismiss()

    def on_ok(self):
        if len(self.url.text) > 0:
            self.add_to_lscam()
        else:
            self.error = True

    def on_cancel(self):
        self.dismiss()

