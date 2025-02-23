import sys, cv2, time, os, datetime
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture
from threading import Thread, Event
import subprocess as sp
from src.utils import helper, kivyhelper
from pathlib import Path
from src.modules import constants

class KivyCameraMain(Image):
    capture = ObjectProperty(None) #cv2 capture
    url = StringProperty('') #link video to play
    resource_type = StringProperty('')
    durationRate = NumericProperty(0) #(%) variable for processbar video
    durationTotal = NumericProperty(0) # total duration fo video
    frameTotal = NumericProperty(1) #total frame of video
    durationCurrent = NumericProperty(0)
    fps = NumericProperty(25)#frame per second: variable for stream
    reconnect = NumericProperty(0)
    event_capture = None
    default_frame = helper._IMAGES_PATH + 'splash.jpg'
    pipe = None
    f_parent = None
    typeOld = StringProperty('')
    category = StringProperty('')
    data_src = None
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

    def set_fps(self, fps):
        self.fps = fps

    def set_default_data(self):
        self.reconnect = 0
        self.durationRate = 0
        self.durationTotal = 0
        self.durationCurrent = 0
        self.frameTotal = 1

    def set_data_source(self, input, category):
        if helper._BASE_PATH+'temp' in self.url:
            self.url_remove = self.url
        self.data_src = input
        self.url = input['url']
        self.resource_type = input['type']
        self.category = category
        self.set_default_data()
        
        if self.pipe is not None:
            self.pipe.kill()
        if self.capture is not None:
            self.capture.release()
        self.stop_update_capture()
        
        try:
            if self.resource_type == "M3U8" or self.resource_type == "VIDEO" or self.resource_type == 'MP4' or self.resource_type == "RTSP":
                timenow = datetime.datetime.timestamp(datetime.datetime.now())
                output = helper._BASE_PATH+'temp/{}.flv'.format(timenow)
                try:
                    if self.resource_type == 'VIDEO' or self.resource_type == 'MP4' or (self.resource_type == "M3U8" and self.category != constants.LIST_TYPE_PRESENTER):
                        _cap = cv2.VideoCapture(self.url)
                        if _cap.isOpened():
                            self.frameTotal = _cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS)*self.fps
                            self.durationTotal = _cap.get(cv2.CAP_PROP_FRAME_COUNT)/_cap.get(cv2.CAP_PROP_FPS)
                        del _cap
                except Exception as e:
                    print("Exception:", e)

                timeout = 3
                command = ["ffmpeg-win/ffmpeg.exe","-y","-nostats","-i",self.url,'-stream_loop','-1',"-i",helper._BASE_PATH+"media/muted2.mp3","-c:v",self.f_parent.gpu,"-c:a","aac","-ar","44100","-ab","128k","-vsync","1","-vf","scale=-1:720","-vb",self.f_parent.v_bitrate,"-r",str(self.fps),'-g',str(self.fps*2),output]
                if self.category == constants.LIST_TYPE_PRESENTER:
                    self.url = self.data_src['rtmp']
                    timeout=4
                    command = ["ffmpeg-win/ffmpeg.exe","-y","-i",self.url,"-vsync","1","-af","aresample=async=1:min_hard_comp=0.100000:first_pts=0","-c:v",self.f_parent.gpu,"-vf","scale=-1:720","-ar","44100","-ab","128k","-vb",self.f_parent.v_bitrate,"-r",str(self.fps),'-g',str(self.fps*2),output]
                elif self.resource_type == "M3U8":
                    timeout=3
                    command = ["ffmpeg-win/ffmpeg.exe","-y","-nostats","-f","hls","-i",self.url,"-vsync","1","-af","aresample=async=1:min_hard_comp=0.100000:first_pts=0","-flags","+global_header","-c:v",self.f_parent.gpu,"-filter_complex","scale=-1:720","-ar","44100", "-ab", "128k","-vb",self.f_parent.v_bitrate,"-r",str(self.fps),'-g',str(self.fps*2),output]
                elif self.resource_type == "RTSP":
                    timeout=4
                    command = ["ffmpeg-win/ffmpeg.exe","-y","-nostats","-rtsp_flags","prefer_tcp","-i",self.url,"-vsync","1","-c:v",self.f_parent.gpu,"-ar","44100","-ab","128k","-vf","scale=-1:720","-vb","6M",'-preset','fast',"-r",str(self.fps),'-g',str(self.fps*2),output]
                    
                si = sp.STARTUPINFO()
                si.dwFlags |= sp.STARTF_USESHOWWINDOW
                self.pipe = sp.Popen(command, startupinfo=si)
                self.url = output
                Clock.schedule_once(self.init_capture ,timeout)
            else:
                Clock.schedule_once(self.init_capture , 0)
        except :
            Clock.schedule_once(self.init_capture , 0)
            print("except add source")
            pass

    def init_capture(self, second):
        try:
            if self.capture is not None:
                self.capture.release()
            self.stop_update_capture()

            if self.resource_type == 'IMG' and '.gif' in self.url:
                self.resource_type = 'GIF'

            if self.resource_type == 'CAMERA':
                self.capture = cv2.VideoCapture(int(self.url))#url index device 0;1;2;3;...
            else:
                self.capture = cv2.VideoCapture(self.url)

            if self.capture is not None and self.capture.isOpened():
                kivyhelper.getApRoot().loading = False
                kivyhelper.getApRoot().main_display_status(True)
                self.reconnect = 0
                self.event_capture = Clock.schedule_interval(self.update, 1.0 / self.fps)
                if self.f_parent is not None:
                    if self.resource_type == "M3U8" or self.resource_type == "VIDEO" or self.category == constants.LIST_TYPE_SCHEDULE or self.typeOld == "M3U8" or self.typeOld == "VIDEO":
                        self.f_parent.refresh_stream()
                    if self.f_parent.isStream is False:
                        self.remove_file_flv()
                self.typeOld = self.resource_type
            else:
                print("cv2.error:")
                if self.capture is not None:
                    self.capture.release()
                if self.reconnect >= 10:
                    self.show_captured_img(self.default_frame)
                    kivyhelper.getApRoot().loading = False
                else:
                    self.reconnect += 1
                    Clock.schedule_once(self.init_capture,1)
                
        except Exception as e:
            print("Exception init_capture:", e)
            if self.capture is not None:
                self.capture.release()
            if self.reconnect >= 10:
                self.show_captured_img(self.default_frame)
            else:
                self.reconnect += 1
                Clock.schedule_once(self.init_capture,1)
    
    def show_captured_img(self, url=None):
        cap = cv2.VideoCapture(url or self.url)
        ret, frame = cap.read()
        if ret:
            self.update_texture_from_frame(frame)
        cap.release()
        del ret, frame, cap
        if self.category == constants.LIST_TYPE_SCHEDULE:
            self.f_parent.start_schedule(True)

    def stop_update_capture(self):
        if self.event_capture is not None:
            self.event_capture.cancel()
    
    def update(self, dt):
        try:
            if self.capture.isOpened():
                # check is get next
                if not self.capture.grab():
                    kivyhelper.getApRoot().main_display_status(False)
                    if self.category == constants.LIST_TYPE_SCHEDULE:
                        #schedule
                        if 'duration' in self.data_src and  self.data_src['duration'] is not None:
                            if (self.data_src['duration'] == 0 or int(self.durationCurrent) >= self.data_src['duration']-1):
                                self.f_parent.process_schedule(1)
                    if self.resource_type == 'GIF':
                        #replay gif image
                        self.capture.release()
                        self.capture = cv2.VideoCapture(self.url)
                else:
                    if self.category == constants.LIST_TYPE_SCHEDULE:
                        #schedule
                        if 'duration' in self.data_src and  self.data_src['duration'] is not None:
                            if self.data_src['duration'] != 0 and int(self.durationCurrent) >= self.data_src['duration']:
                                self.f_parent.process_schedule(1)

                    ret, frame = self.capture.retrieve()
                    if ret:
                        if self.resource_type == 'VIDEO' or self.resource_type == 'MP4' or self.resource_type == 'M3U8' or self.resource_type == 'RTSP':
                            if self.resource_type == 'VIDEO' or self.resource_type == 'MP4':
                                self.durationRate = self.capture.get(cv2.CAP_PROP_POS_FRAMES) / self.frameTotal
                            self.durationCurrent = self.capture.get(cv2.CAP_PROP_POS_FRAMES)/self.capture.get(cv2.CAP_PROP_FPS)
                        self.update_texture_from_frame(frame)
            else:
                print("update: dont open")
        except IOError:
            print("Exception update:")

    def update_texture_from_frame(self, frame):
        try:
            if self.resource_type in ["IMG","GIF"]:
                frame = self.resizeFrame(frame)
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.flip_vertical()
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
        if frame.shape[0] >= 720:
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