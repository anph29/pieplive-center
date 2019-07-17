import sys, cv2, time, os, datetime
from kivy.uix.image import Image
from kivy.clock import Clock, mainthread
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture
from src.modules.rightcontentview.itemcamera import ItemCamera
from threading import Thread, Event
import subprocess as sp
from src.utils import helper
from pathlib import Path

class KivyCameraMain(Image):
    capture = ObjectProperty(None)
    crFrame = ObjectProperty(None)
    name = StringProperty('')
    url = StringProperty('')
    resource_type = StringProperty('')
    buffer_rate = NumericProperty(0)
    duration_total = StringProperty('00:00:00')#show view
    duration_total_n = NumericProperty(1)
    duration = StringProperty('00:00:00')#show view
    duration_num = NumericProperty(0)
    duration_fps = NumericProperty(25)
    reconnect = NumericProperty(0)

    event_capture = None
    default_frame = helper._IMAGES_PATH + 'splash.jpg'
    pipe = None
    pipe2 = None
    f_parent = None
    typeOld = StringProperty('')
    category = StringProperty('')
    data_src = None
    schedule_type = StringProperty('')

    def __init__(self, **kwargs):
        super(KivyCameraMain, self).__init__(**kwargs)
        self.f_height = 720
        self.show_captured_img(self.default_frame)
        self.stop = Event()

    def set_data_source(self, input, category):
        self.data_src = input
        self.name = input['name']
        self.url = input['url']
        self.resource_type = input['type']
        self.category = category
        self.buffer_rate = 0
        self.duration_total = '00:00:00'
        self.duration = '00:00:00'
        self.duration_num = 0
        self.duration_total_n = 1
        self.duration_fps = 25
        self.schedule_type = ''# '' / duration / end

        if self.category == "SCHEDULE":
            self.schedule_type = 'duration'
        
        if self.pipe is not None:
            self.pipe.kill()
        if self.pipe2 is not None:
            self.pipe2.kill()
        if self.capture is not None:
            self.capture.release()
        self.stop_update_capture()
        fps = 25
        dura = 0
        try:
            if self.resource_type == "M3U8" or self.resource_type == "VIDEO":
                
                try:
                    _cap = cv2.VideoCapture(self.url)
                    if _cap.isOpened():
                        fps = _cap.get(cv2.CAP_PROP_FPS)
                        print('*******************')
                        print('******',fps,'*******')
                        print('*******************')
                        if self.resource_type == 'VIDEO':
                            if fps >= 25:
                                self.duration_total_n = _cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS)*25
                                self.duration_total = helper.convertSecNoToHMS(_cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS))
                                dura = int(_cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS))
                            else:
                                self.duration_total_n = _cap.get(cv2.CAP_PROP_FRAME_COUNT)
                                self.duration_total = helper.convertSecNoToHMS(_cap.get(cv2.CAP_PROP_FRAME_COUNT)/25)
                                dura = int(_cap.get(cv2.CAP_PROP_FRAME_COUNT)/25)
                    del _cap
                except Exception as e:
                    print("Exception:", e)
                        
                if self.category == "SCHEDULE" and dura == self.data_src['duration']:
                    self.schedule_type = 'end'
                output = self.f_parent.url_flv
                timeout = 1
                command = ["ffmpeg-win/ffmpeg.exe","-y","-i",self.url,'-stream_loop','-1',"-i", "../resource/media/muted2.mp3","-ar","44100","-ab", "320k","-vb",self.f_parent.v_bitrate,"-crf", "21", "-preset", "veryfast","-r","25",'-g','25','-threads', '2',output]
                
                if self.resource_type == "M3U8":
                    output = self.f_parent.url_flv_hls
                    timeout=0
                    command = ["ffmpeg-win/ffmpeg.exe","-y","-f", "hls","-i", self.url,"-pix_fmt", "yuv420p", "-vsync", "1","-flags","+global_header", "-crf", "21", "-preset", "veryfast","-ar","44100", "-ab", "320k","-vb",self.f_parent.v_bitrate,"-r","25",'-g','25','-threads', '2',output]
                else: 
                    if fps < 25:
                        command = ["ffmpeg-win/ffmpeg.exe","-y","-i",self.url,'-stream_loop','-1',"-i", "../resource/media/muted2.mp3","-ab", "320k","-af", f"atempo={25/fps}","-vf", f"setpts={fps/25}*PTS","-vb",self.f_parent.v_bitrate,"-r","25",'-threads', '2',output]
                    if self.typeOld == 'M3U8':
                        command2 =  f'ffmpeg-win/ffmpeg.exe -y -loop 1 -i {self.default_frame} -i ../resource/media/muted.mp3 -filter_complex:0 "scale=-1:720,pad=1280:720:(1280-iw)/2:(720-ih)/2,setsar=1" -filter_complex:1 "volume=0" -r 25 {self.f_parent.url_flv_hls}'
                        si = sp.STARTUPINFO()
                        si.dwFlags |= sp.STARTF_USESHOWWINDOW
                        self.pipe2 = sp.Popen(command2, startupinfo=si)
                        Clock.schedule_once(lambda x: self.pipe2.kill() , 5)
                
                si = sp.STARTUPINFO()
                si.dwFlags |= sp.STARTF_USESHOWWINDOW
                self.pipe = sp.Popen(command, startupinfo=si)
                self.url = output
                Clock.schedule_once(self.process_set_data ,timeout)
            else:
                if self.typeOld == 'M3U8' or self.typeOld == 'VIDEO':
                    command =  f'ffmpeg-win/ffmpeg.exe -y -loop 1 -i {self.default_frame} -i ../resource/media/muted.mp3 -filter_complex:0 "scale=-1:720,pad=1280:720:(1280-iw)/2:(720-ih)/2,setsar=1" -filter_complex:1 "volume=0" -r 25 {self.f_parent.url_flv} {self.f_parent.url_flv_hls}'
                    si = sp.STARTUPINFO()
                    si.dwFlags |= sp.STARTF_USESHOWWINDOW
                    self.pipe = sp.Popen(command, startupinfo=si)
                    Clock.schedule_once(lambda x: self.pipe.kill() , 5)
                Clock.schedule_once(self.process_set_data , 0)
        except Exception as e:
            print("Exception:", e)
            Clock.schedule_once(self.process_set_data , 0)
        
    def process_set_data(self, second):
        try:
            self.stop.set()
            th = Thread(target=self.init_capture())
            th.start()
            # self.init_capture()
        except Exception:
            pass

    def init_capture(self):
        try:
            if self.capture is not None:
                self.capture.release()
            self.stop_update_capture()
            if self.resource_type == 'IMG':
                self.show_captured_img(self.url)
            else:
                if self.resource_type == 'CAMERA':
                    self.capture = cv2.VideoCapture(int(self.url))
                else:
                    self.capture = cv2.VideoCapture(self.url)
                print('url-----',self.url)

                if self.capture is not None and self.capture.isOpened():
                    self.reconnect = 0
                    if self.resource_type != 'VIDEO' and self.resource_type != "M3U8":
                        self.duration_fps = self.capture.get(cv2.CAP_PROP_FPS)
                    print(">>CAPTURE FINED:")
                    self.event_capture = Clock.schedule_interval(self.update, 1.0 / self.duration_fps)
                    if self.f_parent is not None:
                        if self.resource_type == "M3U8" or self.resource_type == "VIDEO":
                            self.f_parent.refresh_stream()
                        elif self.typeOld == "M3U8" or self.typeOld == "VIDEO":
                            self.f_parent.refresh_stream()
                        if self.schedule_type == 'duration':
                            self.f_parent.start_schedule(True)
                    self.typeOld = self.resource_type
                else:
                    print("cv2.error:")
                    if self.reconnect >= 3:
                        if self.capture is not None:
                            self.capture.release()
                        self.show_captured_img(self.default_frame)
                    else:
                        self.reconnect += 1
                        self.init_capture()
                
        except Exception as e:
            print("Exception init_capture:", e)
    
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

    @mainthread
    def update(self, dt):
        try:
            # check is get next
            if not self.capture.grab():
                if self.category == 'SCHEDULE':
                    if 'duration' in self.data_src and  self.data_src['duration'] is not None:
                        if int(self.duration_num) >= self.data_src['duration'] and self.schedule_type == 'end':
                            self.f_parent.process_schedule(1)

            elif self.capture.isOpened():
                ret, frame = self.capture.retrieve()
                if ret:
                    if self.resource_type == 'VIDEO' or self.resource_type == 'M3U8':
                        if self.resource_type == 'VIDEO':
                            self.buffer_rate = self.capture.get(cv2.CAP_PROP_POS_FRAMES) / self.duration_total_n
                        self.duration_num = self.capture.get(cv2.CAP_PROP_POS_FRAMES)/self.capture.get(cv2.CAP_PROP_FPS)
                        self.duration = helper.convertSecNoToHMS(self.duration_num)
                    self.update_texture_from_frame(frame)
        except IOError:
            print("Exception update:")

    @mainthread
    def update_texture_from_frame(self, frame):
        try:
            frame = self.resizeFrame(frame)
            fshape = frame.shape
            texture = Texture.create(size=(fshape[1], fshape[0]), colorfmt='bgr')
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture
            del frame
        except IOError:
            print("Exception update_texture_from_frame:")

    def release(self):
        if self.pipe is not None:
            self.pipe.kill()
        if self.pipe2 is not None:
            self.pipe2.kill()
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
