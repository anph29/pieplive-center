import kivy
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from src.modules.custom.filechoose import FileChooser
from src.utils import ftype, helper, scryto
import src.utils.kivyhelper as kv_helper
import cv2

Builder.load_file('src/ui/addschedule.kv')

class AddSchedule(Popup):
    name = ObjectProperty()
    duration = ObjectProperty()
    error = BooleanProperty(False)

    def __init__(self, parent, _data):
        super(AddSchedule, self).__init__()
        self.data = _data
        self.name.text = self.data['name']
        try:
            if self.data['type'] == 'VIDEO':
                _cap = cv2.VideoCapture(self.data['url'])
                if _cap.isOpened():
                    self.duration.text = str(int(_cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS)))
                del _cap
        except Exception as e:
            print("Exception:", e)

    def add_to_schedule(self):
        helper._add_to_schedule({
            "id":scryto.hash_md5_with_time(self.data['url']),
            "name": self.name.text,
            "url": self.data['url'],
            "type": self.data['type'],
            "duration": int(self.duration.text)
        })
        kv_helper.getApRoot().init_right_content_schedule()
        self.dismiss()

    def on_ok(self):
        # if isinstance(self.duration.text, int):
        try:
            if len(self.duration.text) > 0:
                self.add_to_schedule()
            else:
                self.error = True
        except Exception:
            self.error = True

    def on_cancel(self):
        self.dismiss()
    
