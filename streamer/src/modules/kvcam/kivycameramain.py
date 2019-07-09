import sys
import cv2
import time
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture
from src.modules.rightcontentview.itemcamera import ItemCamera
from threading import Thread, Event
import subprocess as sp
import src.utils.helper as helper

class KivyCameraMain(Image):
    capture = ObjectProperty(None)
    crFrame = ObjectProperty(None)
    name = StringProperty('')
    url = StringProperty('')
    resource_type = StringProperty('')
    buffer_rate = NumericProperty(0)
    duration_total = StringProperty('00:00:00')
    duration_total_n = NumericProperty(1)
    duration = StringProperty('00:00:00')
    duration_fps = NumericProperty(25)

    event_capture = None
    default_frame = 'src/images/splash.jpg'
    pipe = None
    f_parent = None
    typeOld = ''

    def __init__(self, **kwargs):
        super(KivyCameraMain, self).__init__(**kwargs)
        self.f_height = 720
        self.show_captured_img(self.default_frame)
        self.stop = Event()

    def set_data_source(self, input):
        self.name = input['name']
        self.url = input['url']
        self.resource_type = input['type']
        self.buffer_rate = 0
        self.duration_total = '00:00:00'
        self.duration = '00:00:00'
        self.duration_total_n = 1
        self.duration_fps = 25
        self.release()
        fps = 25
        try:
            if self.resource_type == "M3U8" or self.resource_type == "VIDEO":
                if self.resource_type == 'VIDEO':
                    try:
                        _cap = cv2.VideoCapture(self.url)
                        if _cap.isOpened():
                            print(self.name,'======',_cap.get(cv2.CAP_PROP_FPS),"======")
                            fps = _cap.get(cv2.CAP_PROP_FPS)
                            if fps >= 25:
                                self.duration_total_n = _cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS)*25
                                self.duration_total = helper.convertSecNoToHMS(_cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS))
                            else:
                                self.duration_total_n = _cap.get(cv2.CAP_PROP_FRAME_COUNT)
                                self.duration_total = helper.convertSecNoToHMS(_cap.get(cv2.CAP_PROP_FRAME_COUNT)/25)
                        del _cap
                    except Exception as e:
                        print("Exception:", e)
                
                command = ["ffmpeg-win/ffmpeg.exe","-y","-i",self.url,'-stream_loop','-1',"-i", "../resource/media/muted2.mp3","-ar","44100","-ab", "320k","-vb","3072k","-r","25","../resource/media/output.flv"]
                if fps < 25:
                    command = ["ffmpeg-win/ffmpeg.exe","-y","-i",self.url,'-stream_loop','-1',"-i", "../resource/media/muted2.mp3","-ar","44100","-ab", "320k","-af", f"atempo={25/fps}","-vf", f"setpts={fps/25}*PTS","-vb","3072k","-r","25","../resource/media/output.flv"]
                
                si = sp.STARTUPINFO()
                si.dwFlags |= sp.STARTF_USESHOWWINDOW
                self.pipe = sp.Popen(command, startupinfo=si)
                
                self.url = '../resource/media/output.flv'
                Clock.schedule_once(self.process_set_data , 1)
            else:
                if self.typeOld == 'M3U8' or self.typeOld == 'VIDEO':
                    command =  'ffmpeg-win/ffmpeg.exe -y -loop 1 -i src/images/splash.jpg -i ../resource/media/muted.mp3 -filter_complex:0 "scale=-1:720,pad=1280:720:(1280-iw)/2:(720-ih)/2,setsar=1" -filter_complex:1 "volume=0" -r 25 ../resource/media/output.flv'
                    si = sp.STARTUPINFO()
                    si.dwFlags |= sp.STARTF_USESHOWWINDOW
                    self.pipe = sp.Popen(command, startupinfo=si)
                    Clock.schedule_once(lambda x: self.pipe.kill() , 5)
                Clock.schedule_once(self.process_set_data , 0)
        except Exception as e:
            print("Exception:", e)
            Clock.schedule_once(self.process_set_data , 0)
        
    def process_set_data(self, second):
        if self.capture is not None:
            self.capture.release()
        self.stop_update_capture()
        th = Thread(target=self.init_capture())
        th.start()

    def init_capture(self):
        try:
            if self.resource_type == 'IMG':
                self.show_captured_img(self.url)
            else:
                if self.resource_type == 'CAMERA':
                    self.capture = cv2.VideoCapture(int(self.url))
                else:
                    self.capture = cv2.VideoCapture(self.url)
                print('url-----',self.url)

                if self.capture is not None and self.capture.isOpened():
                    if self.f_parent is not None:
                        if self.resource_type == "M3U8" or self.resource_type == "VIDEO":
                            self.f_parent.refresh_stream()
                        elif self.typeOld == "M3U8" or self.typeOld == "VIDEO":
                            self.f_parent.refresh_stream()
                    self.typeOld = self.resource_type
                    self.duration_fps = round(self.capture.get(cv2.CAP_PROP_FPS))
                    print(">>CAPTURE FINED:")
                    self.event_capture = Clock.schedule_interval(self.update, 1.0 / self.duration_fps)
                else:
                    print("cv2.error:")
                    if self.capture is not None:
                        self.capture.release()
                    self.show_captured_img(self.default_frame)
        except Exception as e:
            print("Exception:", e)
    
    def _process(self):
        self.event_capture = Clock.schedule_interval(self.update, 1.0 / self.duration_fps)
    
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
            # check is get next
            if not self.capture.grab():
                return False
            # playing
            if self.capture.isOpened():
                ret, frame = self.capture.retrieve()
                if ret:
                    if self.resource_type == 'VIDEO':
                        self.buffer_rate = self.capture.get(cv2.CAP_PROP_POS_FRAMES) / self.duration_total_n
                        self.duration = helper.convertSecNoToHMS(self.capture.get(cv2.CAP_PROP_POS_FRAMES)/self.capture.get(cv2.CAP_PROP_FPS))
                    self.update_texture_from_frame(frame)
        except IOError:
            return False

    def update_texture_from_frame(self, frame):
        frame = self.resizeFrame(frame)
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

    def resizeFrame(self, frame):
        if frame is None:
            return frame
        h, w, c = frame.shape
        r = w / h
        nH = self.f_height
        nW = int(nH * r)
        return cv2.resize(frame, (nW, nH), interpolation=cv2.INTER_AREA)
