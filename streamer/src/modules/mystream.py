from src.utils import helper, kivyhelper
from threading import Thread, Event
from kivy.clock import Clock, mainthread
from kivy.graphics import Fbo, ClearColor, ClearBuffers, Scale, Translate
from kivy.uix.relativelayout import RelativeLayout
from src.modules.custom.pieplabel import PiepLabel
from src.modules.custom.piepimage import PiepImage
from kivy.properties import ObjectProperty,NumericProperty
from kivy.lang import Builder
from src.models.normal_model import Normal_model
import subprocess, cv2, os

class MyStream():
    f_parent= ObjectProperty(None)

    def __init__(self, context, f_width, f_height, **kwargs):
        super(MyStream, self).__init__(**kwargs)
        self.f_width = f_width
        self.f_height = f_height
        self.context = context
        self.fps = 25
        self.v_bitrate = "3072k"
        self.urlStream = ''
        self.devAudio = None
        self.deviceVolume = 100
        self.isStream = False
        self.isRecord = False
        self.pipe = None
        self.pipe2 = None
        self.lsSource = []
        self.command = []
        self.event = None
        self.canvas_parent_index = 0
        self.stop = Event()
        self.reconnect = 0

    def set_file_temp(self, url_flv, url_flv_hls, mini_url_flv, mini_url_flv_hls):
        self.url_flv = url_flv
        self.url_flv_hls = url_flv_hls
        self.mini_url_flv = mini_url_flv
        self.mini_url_flv_hls = mini_url_flv_hls

    def _set_source(self,lsSource):
        self.lsSource = lsSource

    def is_streaming(self):
        return self.isStream

    def record(self):
        if self.record:
            self.isRecord = False
        else:
            self.isRecord = True

    def startStream(self):
        try:
            if self.event is not None:
                self.event.cancel()
            self.fbo = Fbo(size=(self.f_width, self.f_height))
            with self.fbo:
                ClearColor(0, 0, 0, 1)
                ClearBuffers()
                Scale(1, -1, 1)
                Translate(-self.x, -self.y - self.f_height, 0)
            self.fbo.add(self.context.canvas)

            self.isStream = True
            # Thread(target=self._process).start()
            self._process()
        except IOError:
            kivyhelper.getApRoot().triggerStop()
        

    def _process(self):
        self.event = Clock.schedule_interval(self.stream, 1/25)

    @mainthread
    def stream(self, fps):
        try:
            if self.isStream:
                # if self.parent is not None:
                #     self.canvas_parent_index = self.parent.canvas.indexof(self.canvas)
                #     if self.canvas_parent_index > -1:
                #         self.parent.canvas.remove(self.canvas)
                # self.fbo.add(self.canvas)
                self.fbo.draw()
                self.pipe.stdin.write(self.fbo.pixels)
                # self.fbo.remove(self.canvas)
                # if self.parent is not None and self.canvas_parent_index > -1:
                #     self.parent.canvas.insert(self.canvas_parent_index, self.canvas)
                self.reconnect = 0
        except:
            self.stopStream()
            self.reconnect += 2
            normal = Normal_model()
            key = self.f_parent.bottom_left.stream_key.text.split("?")[0]
            normal.reset_link_stream(key)
            Clock.schedule_once(self.reconnecting,self.reconnect)
            
    def reconnecting(self, dt):
        if self.reconnect > 10:
            kivyhelper.getApRoot().triggerStop()
        else:
            if bool(self.prepare()):
                self.startStream()
    
    def stopStream(self):
        self.isStream = False
        if self.event is not None:
            self.event.cancel()
        if self.pipe is not None:
            self.pipe.kill()
        if self.stop is not None:
            self.stop.set()
        self.fbo.remove(self.context.canvas)
        # if self.parent is not None and self.canvas_parent_index > -1:
        #     self.parent.canvas.insert(self.canvas_parent_index, self.canvas)
        print("--- STOP ---")
        
    def set_url_stream(self, urlStream):
        self.urlStream = urlStream

    def set_device_audio(self, devAudio):
        self.devAudio = devAudio

    def draw_element(self):
        numau = 0
        inp = []
        txt = _map = ''

        numau += 1
        inp.extend(['-stream_loop','-1',"-i", '../resource/media/muted.mp3'])
        txt += f"[{numau}:a]volume=0[a{numau}];"
        _map += f'[a{numau}]'

        if self.camera.resource_type == "VIDEO" or self.camera.resource_type == "M3U8":
            url = self.url_flv
            if self.camera.resource_type == "M3U8":
                url = self.url_flv_hls
            numau += 1
            if self.camera.duration_current == 0:
                inp.extend(["-i", url])
            else:
                inp.extend(["-ss", helper.convertSecNoToHMS(self.camera.duration_current),"-i", url,"-flags","+global_header"])
            txt += f"[{numau}:a]volume=1[a{numau}];"
            _map += f'[a{numau}]'

        if self.f_parent.showMiniD is True:
            url = self.mini_url_flv
            if self.cameraMini.resource_type == "M3U8":
                url = self.mini_url_flv_hls
            numau += 1
            if self.cameraMini.duration_current == 0:
                inp.extend(["-i", url])
            else:
                inp.extend(["-ss", helper.convertSecNoToHMS(self.cameraMini.duration_current),"-i", url,"-flags","+global_header"])
            txt += f"[{numau}:a]volume=1[a{numau}];"
            _map += f'[a{numau}]'

        if 'audio' in self.camera.data_src:
            if self.camera.data_src['audio'] != '':
                inp.extend(['-stream_loop','-1',"-i", self.camera.data_src['audio']])
                numau += 1
                txt += f'[{numau}:a]volume=1[a{numau}];'
                _map += f'[a{numau}]'

        if len(self.lsSource) > 0:
            for value in self.lsSource:
                if value['active'] == 1:
                    if value['type'] == 'audio' and os.path.exists(value['src']) is True:
                        inp.extend(['-stream_loop','-1',"-i", value['src']])
                        numau += 1
                        txt += f'[{numau}:a]volume={str(value["volume"]/100)}[a{numau}];'
                        _map += f'[a{numau}]'
        if self.devAudio is not None:
            inp.extend(['-f', 'dshow', '-i', 'audio={}'.format(self.devAudio)])
            numau += 1
            txt += f"[{numau}:a]volume={str(self.deviceVolume/100)}[a{numau}];"
            _map += f'[a{numau}]'

        if numau > 0:
            txt += _map + f'amix={str(numau)}[a]'

        if len(txt) > 0:
            inp.extend(['-filter_complex', txt,'-map','0:v', '-map','[a]'])
            
        return inp

    def prepare(self):
        try:
            self.command = ['ffmpeg-win/ffmpeg.exe','-y','-framerate', '25','-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '{}x{}'.format(self.f_width, self.f_height), '-i', '-']
            
            self.command.extend(self.draw_element())
            # encode
            self.command.extend(['-vb', str(self.v_bitrate),'-r', '25', '-pix_fmt', 'yuv420p','-g','60'])

            self.command.extend(["-vf", "fps=25",'-metadata', 'title="PiepLiveCenter"'])
            # tream
            self.command.extend(['-f', 'flv', self.urlStream])
            
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.pipe = subprocess.Popen(self.command, stdin=subprocess.PIPE, startupinfo=si)
            return True

        except IOError:
            print("Exception prepare:")
            return False
            
    def prepare_audio(self):
        pass

    def release(self):
        try:
            if self.event is not None:
                self.event.cancel()
            if self.pipe is not None:
                self.pipe.kill()
            if self.pipe2 is not None:
                self.pipe2.kill()
            if os.path.exists(self.url_flv):
                os.remove(self.url_flv)
            if os.path.exists(self.url_flv_hls):
                os.remove(self.url_flv_hls)
            if os.path.exists(self.mini_url_flv):
                os.remove(self.mini_url_flv)
            if os.path.exists(self.mini_url_flv_hls):
                os.remove(self.mini_url_flv_hls)
        except IOError:
            print("Exception prepare:")
            return False

    def on_change_Volume(self, idx, value):
        if idx is not None and value is not None:
            if idx != -1:
                for _s in self.lsSource:
                    if _s['idx'] == idx:
                        _s['volume'] = value
                        helper._write_lsStaticSource(self.lsSource)
                        break
            else:
                self.deviceVolume = value

            if self.isStream is True:
                self.pipe.kill()
                self.prepare()

    def on_change_audio(self):
        if self.isStream is True:
            self.pipe.kill()
            self.prepare()