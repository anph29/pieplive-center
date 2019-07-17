import sys
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture
from kivy.uix.behaviors import DragBehavior
from kivy.graphics import Rectangle, Color
from src.modules.rightcontentview.itemcamera import ItemCamera
from threading import Thread, Event
import subprocess as sp
from kivy.lang import Builder
from functools import partial
from src.utils import helper

_CAM_NUMS_FRAME = '-2562047788015215'

kv = '''
<KivyCameraMini>:
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
    keep_ratio: True
'''

Builder.load_string(kv)

class KivyCameraMini(DragBehavior, Image):
    capture = ObjectProperty(None)
    crFrame = ObjectProperty(None)
    name = StringProperty('')
    url = StringProperty('')
    resource_type = StringProperty('')
    event_capture = None
    default_frame = helper._IMAGES_PATH + 'splash.jpg'
    pipe = None
    f_parent = None
    typeOld = ''
    data_src = None

    def __init__(self, **kwargs):
        super(KivyCameraMini, self).__init__(**kwargs)
        self.show_captured_img(self.default_frame)
        self.stop = Event()

    def on_touch_up(self, touch):
        if self._get_uid('svavoid') in touch.ud:
            return super(DragBehavior, self).on_touch_up(touch)

        if self._drag_touch and self in [x() for x in touch.grab_list]:
            touch.ungrab(self)
            self._drag_touch = None
            ud = touch.ud[self._get_uid()]
            if ud['mode'] == 'unknown':
                super(DragBehavior, self).on_touch_down(touch)
                Clock.schedule_once(partial(self._do_touch_up, touch), .1)
        else:
            if self._drag_touch is not touch:
                super(DragBehavior, self).on_touch_up(touch)
        return self._get_uid() in touch.ud

    def set_data_source(self, input):
        if self.capture is not None:
            self.capture.release()
        self.stop_update_capture()
        self.data_src = input
        self.name = input['name']
        self.url = input['url']
        self.resource_type = input['type']
        self.release()
        self.init_capture()

    def init_capture(self):
        try:
            if self.resource_type == 'IMG':
                self.show_captured_img(self.url)
            else:
                if self.resource_type == 'CAMERA':
                    self.capture = cv2.VideoCapture(int(self.url))
                else:
                    self.capture = cv2.VideoCapture(self.url)

                if self.capture is not None and self.capture.isOpened():
                    print(">>CAPTURE FINED:")
                    self.event_capture = Clock.schedule_interval(self.update, 1.0 / 30)
                else:
                    print("cv2.error:")
                    if self.capture is not None:
                        self.capture.release()
                    self.show_captured_img(self.default_frame)
        except cv2.error as e:
            print("cv2.error:", e)
        except Exception as e:
            print("Exception:", e)
    
    def _process(self):
        self.event_capture = Clock.schedule_interval(self.update, 1.0 / 30)
    
    def show_captured_img(self, url=None):
        cap = cv2.VideoCapture(url or self.url)
        ret, frame = cap.read()
        if ret:
            self.update_texture_from_frame(frame)
        cap.release()
        del ret, frame, cap

    def stop_update_capture(self):
        if self.event_capture is not None:
            self.event_capture.cancel()

    def update(self, dt):
        try:
            # stoped
            if not self.capture.grab():
                return False
            # playing
            if self.capture.isOpened():
                ret, frame = self.capture.retrieve()
                if ret:
                    self.update_texture_from_frame(frame)

        except IOError:
            print('update interval fail--')
            return False

    def update_texture_from_frame(self, frame):
        fshape = frame.shape
        texture = Texture.create(size=(fshape[1], fshape[0]), colorfmt='bgr')
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture
        del frame

    def release(self):
        if self.pipe is not None:
            self.pipe.kill()
        if self.capture is not None:
            self.capture.release()
