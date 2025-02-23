import sys
import cv2
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture

class LabelCamera(Label):
    is_playing = BooleanProperty(False)
    capture = ObjectProperty(None)
    crFrame = ObjectProperty(None)
    name = StringProperty('')
    url = StringProperty('')
    resource_type = StringProperty('')
    data_src = None

    def __init__(self, **kwargs):
        super(LabelCamera, self).__init__(**kwargs)

    def set_data_source(self, input):
        self.data_src = input
        self.name = input['name']
        self.text = input['name']
        self.url = input['url']
        self.resource_type = input['type']
        capture = None
        if 'capture' in input and input['capture'] is not None:
            capture = input['capture']
        self.init_capture(capture)

    def get_data_source(self):
        return self.data_src

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

    def play(self):
        is_playing = True

    def pause(self):
        is_playing = False
