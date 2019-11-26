import cv2, subprocess, os, datetime
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.graphics.texture import Texture
from kivy.uix.behaviors import DragBehavior
from kivy.graphics import Rectangle, Color
from threading import Thread, Event
from kivy.lang import Builder
from functools import partial
from src.utils import helper, kivyhelper
from src.modules import constants

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
    url = StringProperty('')
    resource_type = StringProperty('')
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
        super(KivyCameraMini, self).__init__(**kwargs)
        self.f_height = 720
        self.show_captured_img(self.default_frame)
        self.data_src = {
            "id": "8c31e461881ac85d932bb461b132f32f",
            "name": "image",
            "url": self.default_frame,
            "type": "IMG"
        }

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

    def set_fps(self, fps):
        self.fps = fps

    def set_default_data(self):
        self.reconnect = 0
        self.durationCurrent = 0

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


                timeout = 2
                command = ["ffmpeg-win/ffmpeg.exe","-y","-nostats","-i",self.url,'-stream_loop','-1',"-i", helper._BASE_PATH+"media/muted2.mp3","-c:v",self.f_parent.gpu,"-af", "aresample=async=1","-ar","44100","-ab", "128k","-vsync","1","-vf","scale=-1:720","-vb",self.f_parent.v_bitrate,"-r",str(self.fps),'-g',str(self.fps*2),output]
                if self.category == constants.LIST_TYPE_PRESENTER:
                    self.url = self.data_src['rtmp']
                    timeout=3
                    command = ["ffmpeg-win/ffmpeg.exe","-y","-nostats","-i",self.url,"-vsync","1","-af","aresample=async=1:min_hard_comp=0.100000:first_pts=0","-c:v",self.f_parent.gpu,"-vf","scale=-1:720","-ar","44100","-ab","128k","-vb",self.f_parent.v_bitrate,'-preset','fast',"-r",str(self.fps),'-g',str(self.fps*2),output]
                elif self.resource_type == "M3U8":
                    timeout=2
                    command = ["ffmpeg-win/ffmpeg.exe","-y","-nostats","-f","hls","-i",self.url,"-vsync", "1","-af","aresample=async=1:min_hard_comp=0.100000:first_pts=0","-flags","+global_header","-c:v",self.f_parent.gpu,"-filter_complex","scale=-1:720","-ar","44100","-ab","128k","-vb",self.f_parent.v_bitrate,"-r",str(self.fps),'-g',str(self.fps*2),output]
                elif self.resource_type == "RTSP":
                    timeout=3
                    command = ["ffmpeg-win/ffmpeg.exe","-y","-nostats","-rtsp_flags","prefer_tcp","-i", self.url,"-flags","+global_header","-vsync","1","-c:v",self.f_parent.gpu,"-ar","44100","-ab","128k","-vf","scale=-1:720","-vb",self.f_parent.v_bitrate,'-preset','fast',"-r",str(self.fps),'-g',str(self.fps*2),output]
                    
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                self.pipe = subprocess.Popen(command, startupinfo=si)
                self.url = output
                Clock.schedule_once(self.init_capture ,timeout)
            else:
                Clock.schedule_once(self.init_capture , 0)
        except :
            print("Exception: source")
            # Clock.schedule_once(self.init_capture , 0)

    def init_capture(self, second):
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
                kivyhelper.getApRoot().loadingMini = False
                kivyhelper.getApRoot().mini_display_status(True)
                self.reconnect = 0
                self.event_capture = Clock.schedule_interval(self.update, 1.0 / self.fps)
                if self.f_parent is not None:
                    if self.resource_type == "M3U8" or self.resource_type == "VIDEO" or self.category == constants.LIST_TYPE_SCHEDULE or self.typeOld == "M3U8" or self.typeOld == "VIDEO":
                        self.f_parent.refresh_stream()
                    if self.f_parent.isStream is False:
                        self.remove_file_flv()
                self.typeOld = self.resource_type
            else:
                if self.capture is not None:
                    self.capture.release()
                if self.reconnect >= 20:
                    self.show_captured_img(self.default_frame)
                    kivyhelper.getApRoot().loadingMini = False
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

    def stop_update_capture(self):
        if self.event_capture is not None:
            self.event_capture.cancel()

    def update(self, dt):
        try:
            if self.capture.isOpened():
                if not self.capture.grab():
                    kivyhelper.getApRoot().mini_display_status(False)
                    if 'list' in self.data_src and self.data_src['list'] == constants.LIST_TYPE_PRESENTER and kivyhelper.getApRoot().showMiniD is True and kivyhelper.getApRoot().right_content.tab_presenter.ls_presenter.check_is_online(self.data_src['id']) is False:
                        self.f_parent.hide_camera_mini(False)
                else:
                    ret, frame = self.capture.retrieve()
                    if ret:
                        if self.resource_type == 'VIDEO' or self.resource_type == 'MP4' or self.resource_type == 'M3U8':
                            self.durationCurrent = self.capture.get(cv2.CAP_PROP_POS_FRAMES)/self.capture.get(cv2.CAP_PROP_FPS)
                        self.update_texture_from_frame(frame)
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
        print('MINICAM','Release')

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