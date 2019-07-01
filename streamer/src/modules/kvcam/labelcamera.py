import sys
import cv2
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture

_CAM_NUMS_FRAME = '-2562047788015215'

class LabelCamera(Label):
    is_playing = BooleanProperty(False)
    capture = ObjectProperty(None)
    crFrame = ObjectProperty(None)
    name = StringProperty('')
    url = StringProperty('')
    resource_type = StringProperty('')

    def __init__(self, **kwargs):
        super(LabelCamera, self).__init__(**kwargs)

    def set_data_source(self, input):
        # if self.capture is not None:
        #     self.capture.release()
        self.name = input['name']
        self.text = input['name']
        self.url = input['url']
        self.resource_type = input['type']
        capture = None
        if 'capture' in input and input['capture'] is not None:
            capture = input['capture']
        self.init_capture(capture)

    def get_data_source(self):
        return {
            'name': self.name,
            'url': self.url,
            'type': self.resource_type,
            'capture': self.capture
        }

    def _play(self):
        # cap = cv2.VideoCapture(self.url)
        # if bool(cap):
        #     self.init_capture()
        pass

    def _pause(self, *args):
        # self.stop_update_capture()
        # if self.resource_type == 'RTSP':
        #     self.capture.release()
        # self.is_playing = False
        pass

    def init_capture(self, capture=None):
        if capture is not None:
            self.capture = capture
        else: 
            self.capture = self.renew_capture()

    def renew_capture(self):
        return None
        try:
            capture = cv2.VideoCapture(self.url)
            if capture.isOpened():
                print(f">>CAPTURE FINED:{self.name}:{self.resource_type}")
                return capture
            else:
                raise NameError(f">> CLOSED CAPTURE:{self.name}")
        except cv2.error as e:
            print("cv2.error:", e)
        except Exception as e:
            print("Exception:", e)
        return None
