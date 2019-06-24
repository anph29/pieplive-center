import sys
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture
from src.modules.rightcontentview.controllers.itemcamera import ItemCamera

_CAM_NUMS_FRAME = '-2562047788015215'


class KivyCamera(Image):
    is_playing = BooleanProperty(False)
    capture = ObjectProperty(None)
    crFrame = ObjectProperty(None)
    name = StringProperty('')
    url = StringProperty('')
    resource_type = StringProperty('')
    buffer_rate = NumericProperty(0)
    fps = 1
    headless = False
    event_capture = None
    default_frame = 'src/images/splash.jpg'

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.show_captured_img(self.default_frame)

    def set_data_source(self, input):
        self.name = input['name']
        self.url = input['url']
        self.source = input['url']
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
        cap = cv2.VideoCapture(self.url)
        if bool(cap):
            self.init_capture()

    def _pause(self, *args):
        self.stop_update_capture()
        if self.resource_type == 'RTSP':
            self.capture.release()
        self.is_playing = False

    def stop_update_capture(self):
        if self.event_capture is not None:
            self.event_capture.cancel()

    def update(self, dt):
        try:
            # stoped
            if not self.capture or not self.capture.grab():
                self.stop_update_capture()
                self.is_playing = False
                return False
            # playing
            if self.capture.isOpened():
                ret, frame = self.capture.retrieve()
                if ret:
                    if self.is_playing == False:
                        self.is_playing = True
                    if self.resource_type == 'VIDEO':
                        self.buffer_rate = self.capture.get(
                            cv2.CAP_PROP_POS_FRAMES) / self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
                    self.update_texture_from_frame(frame)

        except IOError:
            print(sys.exc_info()[0], 'update interval fail--')

    def update_texture_from_frame(self, frame):
        fshape = frame.shape
        # re-innit texture
        if fshape[0] != self.texture_shape[0] or fshape[1] != self.texture_shape[1]:
            self.texture_shape = frame.shape
            self.image_texture = Texture.create(
                size=(fshape[1], fshape[0]), colorfmt='bgr')

        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        self.image_texture.blit_buffer(
            buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = self.image_texture

    # let openGL do not need resize
    # def resizeFrame(self, frame):
    #     if frame is None:
    #         return frame
    #     h, w, c = frame.shape
    #     r = w / h
    #     nH = self.f_height
    #     nW = int(nH * r)
    #     return cv2.resize(frame, (nW, nH), interpolation=cv2.INTER_AREA)

    def show_captured_img(self, url=None):
        frame = cv2.imread(url or self.url)
        self.texture_shape = frame.shape
        self.image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        self.update_texture_from_frame(frame)

    def init_capture(self, capture=None):
        # 1.
        if self.resource_type == 'IMG':
            self.show_captured_img()
        else:
            # 2.
            self.capture = capture if capture is not None else self.renew_capture()
            # 3. headless dont need play
            if not self.headless:
                if self.capture is not None:
                    self.fps = self.capture.get(cv2.CAP_PROP_FPS) or 30
                    # 4. low cam, low fps
                    if isinstance(self.parent, ItemCamera):
                        self.parent.dt_capture = self.capture
                        self.fps = 8
                    # 5. re-init interval
                    self.stop_update_capture()
                    self.event_capture = Clock.schedule_interval(
                        self.update, 1.0 / self.fps)

    def renew_capture(self):
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


class KivyCameraLow(KivyCamera):
    def __init__(self, **kwargs):
        super(KivyCameraLow, self).__init__(**kwargs)
        self.default_frame = 'src/images/live-default.jpg'


class KivyCameraHeadless(KivyCamera):
    def __init__(self, **kwargs):
        self.default_frame = 'src/images/live-default.jpg'
        self.headless = True
        super(KivyCameraHeadless, self).__init__(**kwargs)
