import sys
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture
from src.modules.rightcontentview.itemcamera import ItemCamera
from threading import Thread, Event
import subprocess

_CAM_NUMS_FRAME = '-2562047788015215'


class KivyCamera(Image):
    capture = ObjectProperty(None)
    crFrame = ObjectProperty(None)
    name = StringProperty('')
    url = StringProperty('')
    resource_type = StringProperty('')
    event_capture = None
    default_frame = 'src/images/splash.jpg'
    pipe = None
    f_parent = None

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.show_captured_img(self.default_frame)
        self.stop = Event()

    def set_data_source(self, input):
        if self.capture is not None:
            self.capture.release()
        self.stop_update_capture()
        self.name = input['name']
        self.url = input['url']
        self.source = input['url']
        self.resource_type = input['type']
        self.release()
        try:
            if self.resource_type == "M3U8":
                # command = ["src/ffmpeg-win/ffmpeg.exe","-y","-i",f"{input['url']}","-ab","128k","-ac","2","-ar","44100","-vb","3072k","-r","25",f"src/export/{'output'}.flv", f"src/export/{'output'}.wav"]
                command = ["src/ffmpeg-win/ffmpeg.exe","-y","-i",f"{input['url']}","-ab","128k","-ac","2","-ar","44100","-vb","3072k","-r","25",f"src/export/{'output'}.flv"]
                self.pipe = subprocess.Popen(command)
                self.url = 'src/export/{}.flv'.format('output')
            # elif self.resource_type == "VIDEO":
            #     command = ["src/ffmpeg-win/ffmpeg.exe","-y","-i",f"{input['url']}","-ab","128k","-ac","2","-ar","44100","src/export/output.wav"]
            #     # command = ["src/ffmpeg-win/ffmpeg.exe","-y","-i",f"{input['url']}","-ab","128k","-ac","2","-ar","44100","-vb","3072k","-r","25",f"src/export/{'output'}.flv", f"src/export/{'output'}.wav"]
            #     self.pipe = subprocess.Popen(command)
            # else:
            #     # command =  'src/ffmpeg -y -i src/musics/muted.mp3 -filter_complex "volume=0" src/export/output.wav'
            #     command = ["src/ffmpeg-win/ffmpeg.exe","-y","-i",f"{input['url']}","-ab","128k","-ac","2","-ar","44100","-vb","3072k","-r","25",f"src/export/{'output'}.flv", f"src/export/{'output'}.wav"]
            #     self.pipe = subprocess.Popen(command)
        except Exception as e:
            print("Exception:", e)

        capture = None
        if 'capture' in input and input['capture'] is not None:
            capture = input['capture']
        self.init_capture(capture)
        # self.f_parent.refresh_stream()

    def init_capture(self, capture=None):
        try:
            if self.resource_type == 'IMG':
                self.show_captured_img(self.url)
            else:
                if capture is not None:
                    self.capture = capture 
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
            if not self.capture or not self.capture.grab():
                #self.stop_update_capture()
                return False
            # playing
            if self.capture.isOpened():
                ret, frame = self.capture.retrieve()
                if ret:
                    self.update_texture_from_frame(frame)

        except IOError:
            print(sys.exc_info()[0], 'update interval fail--')

    def update_texture_from_frame(self, frame):
        fshape = frame.shape
        texture = Texture.create(size=(fshape[1], fshape[0]), colorfmt='bgr')
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture

    def release(self):
        if self.pipe is not None:
            self.pipe.kill()
