import sys, cv2, time, os, datetime
from kivy.uix.image import Image
from kivy.clock import Clock, mainthread
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture
from threading import Thread, Event
import subprocess as sp
from src.utils import helper, kivyhelper
from pathlib import Path
# from pydub import AudioSegment
# from pydub.playback import play

class KivyCameraMain(Image):
    capture = ObjectProperty(None)
    url = StringProperty('')
    resource_type = StringProperty('')
    buffer_rate = NumericProperty(0)
    duration_total = NumericProperty(0)
    duration_total_n = NumericProperty(1)
    duration_current = NumericProperty(0)
    duration_fps = NumericProperty(25)
    reconnect = NumericProperty(0)

    event_capture = None
    default_frame = helper._IMAGES_PATH + 'splash.jpg'
    pipe = None
    f_parent = None
    typeOld = StringProperty('')
    category = StringProperty('')
    data_src = None
    schedule_type = StringProperty('')
    url_remove = StringProperty('')


    def __init__(self, **kwargs):
        super(KivyCameraMain, self).__init__(**kwargs)
        self.f_height = 720
        self.show_captured_img(self.default_frame)
        self.data_src = {
            "id": "8c31e461881ac85d932bb461b132f32f",
            "name": "image",
            "url": self.default_frame,
            "type": "IMG"
        }

    def set_data_source(self, input, category):
        self.url_remove = self.url
        self.data_src = input
        self.url = input['url']
        self.resource_type = input['type']
        self.category = category
        self.reconnect = 0
        self.buffer_rate = 0
        self.duration_total = 0
        self.duration_current = 0
        self.duration_total_n = 1
        self.duration_fps = 25
        self.schedule_type = ''# '' / duration / end
        if self.category == "SCHEDULE":
            self.schedule_type = 'duration'
            if self.data_src['duration'] == 0:
                self.schedule_type = 'end'
        
        if self.pipe is not None:
            self.pipe.kill()
        if self.capture is not None:
            self.capture.release()
        self.stop_update_capture()
        fps = 25
        dura = 0
        try:
            if self.resource_type == "M3U8" or self.resource_type == "VIDEO" or self.resource_type == 'MP4':# or self.resource_type == "RTSP":
                timenow = datetime.datetime.now().strftime("%d%m%y%H%M%S")
                output = helper._BASE_PATH+'temp/{}.flv'.format(timenow)
                try:
                    _cap = cv2.VideoCapture(self.url)
                    if _cap.isOpened():
                        fps = _cap.get(cv2.CAP_PROP_FPS)
                        print('============',fps,'==========')
                        if self.resource_type == 'VIDEO' or self.resource_type == 'MP4':
                            if fps >= 25:
                                self.duration_total_n = _cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS)*25
                                self.duration_total = _cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS)
                                dura = int(_cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS))
                            else:
                                self.duration_total_n = _cap.get(cv2.CAP_PROP_FRAME_COUNT)
                                self.duration_total = _cap.get(cv2.CAP_PROP_FRAME_COUNT)/25
                                dura = int(_cap.get(cv2.CAP_PROP_FRAME_COUNT)/25)
                    del _cap
                except Exception as e:
                    print("Exception:", e)
                        
                if self.category == "SCHEDULE" and dura == self.data_src['duration']:
                    self.schedule_type = 'end'

                timeout = 1
                command = ["ffmpeg/ffmpeg.exe","-y","-nostats","-i",self.url,'-stream_loop','-1',"-i", helper._BASE_PATH+"media/muted2.mp3","-ar","44100","-ab", "160k","-vb",self.f_parent.v_bitrate,"-r","25",output, output.replace('.flv','.wav')]
                if self.category == "PRESENTER":
                    self.url = self.data_src['rtmp']
                    timeout=2
                    command = ["ffmpeg/ffmpeg.exe","-y","-i", self.url,"-vsync","1","-af","aresample=async=1:min_hard_comp=0.100000","-preset","medium","-ar","44100","-ab","160k","-vb",self.f_parent.v_bitrate,"-r","25",output]
                elif self.resource_type == "M3U8":
                    timeout=1
                    command = ["ffmpeg/ffmpeg.exe","-y","-nostats","-f", "hls","-i", self.url, "-vsync", "1","-af", "aresample=async=1:min_hard_comp=0.100000:first_pts=0","-flags","+global_header","-ar","44100", "-ab", "160k","-vb",self.f_parent.v_bitrate,"-r","25",output]
                elif self.resource_type == "RTSP":
                    timeout=2
                    command = ["ffmpeg/ffmpeg.exe","-y","-nostats","-rtsp_flags", "prefer_tcp","-i", self.url,"-pix_fmt", "yuv420p", "-flags","+global_header", "-vsync","1","-af","aresample=async=1","-ar","44100", "-ab", "160k","-af", "aresample=async=1:min_hard_comp=0.100000:first_pts=0","-vb",self.f_parent.v_bitrate,"-r","25",output]
                else:
                    if fps < 25:
                        command = ["ffmpeg/ffmpeg.exe","-y","-nostats","-i",self.url,'-stream_loop','-1',"-i", helper._BASE_PATH+"media/muted2.mp3","-ar","44100","-ab", "160k","-af", f"atempo={25/fps}","-vf", f"setpts={fps/25}*PTS","-vb",self.f_parent.v_bitrate,"-r","25",output,output.replace('.flv','.wav')]
                    
                si = sp.STARTUPINFO()
                si.dwFlags |= sp.STARTF_USESHOWWINDOW
                self.pipe = sp.Popen(command, startupinfo=si)
                self.url = output
                Clock.schedule_once(self.process_set_data ,timeout)
            else:
                Clock.schedule_once(self.process_set_data , 0)
        except :
            Clock.schedule_once(self.process_set_data , 0)
        
    def process_set_data(self, second):
        try:
            self.init_capture()
        except Exception:
            pass

    def init_capture(self):
        try:
            if self.capture is not None:
                self.capture.release()
            self.stop_update_capture()

            if self.resource_type == 'IMG' and '.gif' in self.url:
                self.resource_type = 'GIF'

            if self.resource_type == 'CAMERA':
                self.capture = cv2.VideoCapture(int(self.url))
            else:
                self.capture = cv2.VideoCapture(self.url)

            if self.capture is not None and self.capture.isOpened():
                kivyhelper.getApRoot().loading = False
                self.reconnect = 0
                self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                # if self.resource_type != 'VIDEO' and self.resource_type != "M3U8":
                #     self.duration_fps = self.capture.get(cv2.CAP_PROP_FPS)
                print(">>CAPTURE FINED:", self.duration_fps)
                self.event_capture = Clock.schedule_interval(self.update, 1.0 / self.duration_fps)
                if self.f_parent is not None:
                    if self.category == "SCHEDULE":
                        self.f_parent.refresh_stream()
                    elif self.resource_type == "M3U8" or self.resource_type == "VIDEO":
                        self.f_parent.refresh_stream()
                    elif self.typeOld == "M3U8" or self.typeOld == "VIDEO":
                        self.f_parent.refresh_stream()
                    if self.schedule_type == 'duration':
                        self.f_parent.start_schedule(True)
                    
                    if self.f_parent.isStream is False:
                        self.remove_file_flv()

                self.typeOld = self.resource_type
                self.playAudio()
            else:
                print("cv2.error:")
                if self.capture is not None:
                    self.capture.release()
                if self.reconnect >= 10:
                    self.show_captured_img(self.default_frame)
                    kivyhelper.getApRoot().loading = False
                else:
                    self.reconnect += 1
                    Clock.schedule_once(self.process_set_data,0.5)
                
        except Exception as e:
            print("Exception init_capture:", e)
            if self.capture is not None:
                self.capture.release()
            if self.reconnect >= 10:
                self.show_captured_img(self.default_frame)
            else:
                self.reconnect += 1
                Clock.schedule_once(self.process_set_data,1)

    def playAudio(self):
        # song = AudioSegment.from_file(self.url.replace('.flv','.wav'))
        # play(song)
        # player = MediaPlayer(self.url)
        pass
    
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
            if self.capture.isOpened():
                # check is get next
                if not self.capture.grab():
                    if self.category == 'SCHEDULE':
                        if 'duration' in self.data_src and  self.data_src['duration'] is not None:
                            if (self.data_src['duration'] == 0 or int(self.duration_current) >= self.data_src['duration']) and self.schedule_type == 'end':
                                self.f_parent.process_schedule(1)
                    if self.resource_type == 'GIF':
                        self.capture.release()
                        self.capture = cv2.VideoCapture(self.url)
                else:
                    ret, frame = self.capture.retrieve()
                    if ret:
                        if self.resource_type == 'VIDEO' or self.resource_type == 'MP4' or self.resource_type == 'M3U8':
                            if self.resource_type == 'VIDEO' or self.resource_type == 'MP4':
                                self.buffer_rate = self.capture.get(cv2.CAP_PROP_POS_FRAMES) / self.duration_total_n
                            self.duration_current = self.capture.get(cv2.CAP_PROP_POS_FRAMES)/self.capture.get(cv2.CAP_PROP_FPS)
                        self.update_texture_from_frame(frame)
        except IOError:
            print("Exception update:")

    def update_texture_from_frame(self, frame):
        try:
            # frame = self.resizeFrame(frame)
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.flip_vertical()
            # buf = cv2.flip(frame, 0).tostring()
            texture.blit_buffer(frame.tostring(), colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture
            del frame, texture
        except IOError:
            print("Exception update_texture_from_frame:")

    def release(self):
        if self.pipe is not None:
            self.pipe.kill()
        if self.capture is not None:
            self.capture.release()
            print('MAINCAM','Release')

    def resizeFrame(self, frame):
        if frame is None:
            return frame
        if frame.shape[1] >= 1280:
            return frame

        h, w, c = frame.shape
        r = w / h
        nH = self.f_height
        nW = int(nH * r)
        return cv2.resize(frame, (nW, nH), interpolation=cv2.INTER_AREA)

    def remove_file_flv(self):
        try:
            if os.path.exists(self.url_remove):
                os.remove(self.url_remove)
        except:
            pass