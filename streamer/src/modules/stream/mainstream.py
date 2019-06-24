import kivy
import subprocess
import cv2
import src.utils.helper as helper
from threading import Thread, Event
from kivy.clock import Clock, mainthread
from kivy.graphics import Fbo, ClearColor, ClearBuffers, Scale, Translate
from kivy.uix.relativelayout import RelativeLayout
from src.modules.kvcam.kivycamera2 import KivyCamera
from src.modules.custom.pieplabel import PiepLabel
from src.modules.custom.piepimage import PiepImage
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from kivy.core.window import Window
from kivy.animation import Animation
from kivy.factory import Factory

import numpy as np
import array
import audioread

Builder.load_file('src/ui/mainstream.kv')
class MainStream(RelativeLayout):
    camera= ObjectProperty()
    f_parent= ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainStream, self).__init__(**kwargs)
        self.f_width = 1280
        self.f_height = 720
        self.capture = None
        self.fps = 30
        self.v_bitrate = "3072k"
        self.urlStream = ''
        self.devAudio = None
        self.deviceVolume = 100
        self.isStream = False
        self.isRecord = False
        self.pipe = None
        self.lsSource = []
        self.command = []
        self.event = None
        self.canvas_parent_index = 0
        self.stop = Event()
        self.dataCam = {
            "name": "defaul",
            "url": "src/images/splash.jpg",
            "type": "IMG"
        }

    def _load(self):
        try:
            command =  'src/ffmpeg-win/ffmpeg.exe -y -loop 1 -i src/images/splash.jpg -i src/musics/muted.mp3 -filter_complex:0 "scale=-1:720,pad=1280:720:(1280-iw)/2:(720-ih)/2,setsar=1" -filter_complex:1 "volume=0" -r 25 src/export/output.flv'
            self.pipe2 = subprocess.Popen(command)
            Clock.schedule_once(lambda x: self.pipe2.kill() , 10)
        except IOError:
            pass
    
    def _set_capture(self, data_src):
        self.dataCam = data_src
        self.camera.f_parent = self
        self.camera.set_data_source(data_src)
        self.refresh_stream()

    def refresh_stream(self):
        if self.isStream is True:
            self.pipe.kill()
            self.prepare()

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
            self.fbo = Fbo(size=(self.f_width, self.f_height))
            with self.fbo:
                ClearColor(0, 0, 0, 1)
                ClearBuffers()
                Scale(1, -1, 1)
                Translate(-self.x, -self.y - self.f_height, 0)
            self.fbo.add(self.canvas)

            self.isStream = True
            Thread(target=self._process).start()
        except IOError:
            helper.getApRoot().triggerStop()
        

    def _process(self):
        self.event = Clock.schedule_interval(self.stream, 1/30)

    def _audio(self):
        with audioread.audio_open('src/videos/xin-mot-lan-ngoai-le.mp4') as f:
            print('------------------------------------',f.channels, f.samplerate, f.duration)
            for buf in f:
                if self.isStream:
                    self.pipe.stdin.write(buf)

    @mainthread
    def stream(self, fps):
        try:
            if self.isStream:
                if self.parent is not None:
                    self.canvas_parent_index = self.parent.canvas.indexof(self.canvas)
                    if self.canvas_parent_index > -1:
                        self.parent.canvas.remove(self.canvas)
                self.fbo.draw()
                self.pipe.stdin.write(self.fbo.pixels)
                self.fbo.remove(self.canvas)
                if self.parent is not None and self.canvas_parent_index > -1:
                    self.parent.canvas.insert(self.canvas_parent_index, self.canvas)
        except IOError:
            helper.getApRoot().triggerStop()
            self.pipe.kill()
            self.fbo.remove(self.canvas)
            if self.event is not None:
                self.event.cancel()
            if self.parent is not None and self.canvas_parent_index > -1:
                self.parent.canvas.insert(self.canvas_parent_index, self.canvas)

    def set_url_stream(self, urlStream):
        self.urlStream = urlStream

    def set_device_audio(self, devAudio):
        self.devAudio = devAudio

    def draw_element(self):
        numau = 0
        inp = []
        txt = ''

        numau += 1
        inp.extend(['-stream_loop','-1',"-i", 'src/musics/default.mp3'])
        txt += "[EMP];[EMP]volume=0"

        if self.dataCam['type'] == "VIDEO" or self.dataCam['type'] == "M3U8":
            url = self.dataCam['url']
            if self.dataCam['type'] == 'M3U8':
                url = 'src/export/output.flv'
            numau += 1
            inp.extend(["-i", url,'-vn'])
            txt += "[EMP];[EMP]volume=1"

        if len(self.lsSource) > 0:
            for value in self.lsSource:
                if value['active'] == 1:
                    if(value['type'] == 'audio'):
                        inp.extend(["-i", value['src']])
                        txt += '[EMP];[EMP]volume={}'.format(str(value['volume']/100))
                        numau += 1
        if self.devAudio is not None:
            inp.extend(['-f', 'dshow', '-i', 'audio={}'.format(self.devAudio)])
            numau += 1
            txt += "[EMP];[EMP]volume={}".format(self.deviceVolume/100)

        if numau > 0:
            txt = 'amix=inputs={}'.format(str(numau)) + txt

        if len(txt) > 0:
            inp.extend(['-filter_complex', txt])
            
        return inp

    def prepare(self):
        try:
            self.command = ['src/ffmpeg-win/ffmpeg.exe','-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '{}x{}'.format(self.f_width, self.f_height), '-i', '-']
            
            self.command.extend(self.draw_element())
            # encode
            self.command.extend(['-vb', str(self.v_bitrate), '-preset', 'veryfast', '-g', '25', '-r', '25'])
            # tream
            self.command.extend(['-f', 'flv', self.urlStream])
            
            self.pipe = subprocess.Popen(self.command, stdin=subprocess.PIPE)
            
            return True

        except IOError:
            return False

    def stopStream(self):
        self.isStream = False
        if self.event is not None:
            self.event.cancel()
        if self.pipe is not None:
            self.pipe.kill()
        # self.fbo.remove(self.mainview.canvas)
        self.fbo.remove(self.canvas)
        if self.stop is not None:
            self.stop.set()
        if self.parent is not None and self.canvas_parent_index > -1:
            self.parent.canvas.insert(self.canvas_parent_index, self.canvas)
        print("--- STOP ---")

    def release(self):
        if self.event is not None:
            self.event.cancel()
        if self.pipe is not None:
            self.pipe.kill()
        if self.camera is not None:
            self.camera.release()
        if self.pipe2 is not None:
            self.pipe2.kill()
        print("--- release ---")

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

    def on_change_position(self, idx, pos_x, pos_y, parentName):
        self.f_parent.on_change_position(idx, pos_x, pos_y)
        # for child in self.mainview.children:
        #     if child.idx == idx:
        #         child.x = pos_x
        #         child.top = pos_y
        #         break

    def show_text(self, text, font, size, color, pos_x, pos_y, active, idx, new):
        if new:
            pText = PiepLabel(text='[color=' + str(color) + ']' + text + '[/color]',
                            font_size=size,
                            font_name=font,
                            x=pos_x,
                            y=pos_y,
                            markup=True,
                            opacity=active,
                            idx=idx,
                            parentName='main')
            self.add_widget(pText)
            # pText2 = PiepLabel(text='[color=' + str(color) + ']' + text + '[/color]',
            #                    font_size=size,
            #                    font_name=font,
            #                    x=pos_x,
            #                    y=pos_y,
            #                    markup=True,
            #                    opacity=active,
            #                    idx=idx,
            #                    parentName='canvas')
            # self.mainview.add_widget(pText2)
        else:
            for child in self.children:
                if child.idx != None and child.idx == idx:
                    child.text = '[color=' + str(color) + ']' + text + '[/color]'
                    child.font_size = str(size)
                    child.font_name = font
                    #child.x = pos_x
                    #child.y = pos_y
                    #child.markup = True
                    #child.opacity = active
                    #child.idx = idx
                    break


    def show_image(self, src, pos_x, pos_y, w, h, active, idx, new):
        if new:
            pimage = PiepImage(source=src,
                            size_hint=(None,None),
                            width=w,
                            height=h,
                            x=pos_x,
                            y=pos_y,
                            opacity=active,
                            idx=idx,
                            parentName='main')
            self.add_widget(pimage)
            # pimage2 = PiepImage(source=src,
            #                    size=(w, h),
            #                    x=pos_x,
            #                    y=pos_y,
            #                    opacity=active,
            #                    idx=idx,
            #                    parentName='canvas')
            # self.mainview.add_widget(pimage2)
        else:
            for child in self.children:
                if child.idx != None and child.idx == idx:
                    child.source = src
                    child.size = (w, h)
                    break

    def on_off_source(self, idx, value):
        for child in self.children:
            if child.idx != None and child.idx == idx:
                if value:
                    child.opacity = 1
                else:
                    child.opacity = 0
                break
        
        # for child in self.mainview.children:
        #     if child.idx != None and child.idx == idx:
        #         if value:
        #             child.opacity = 1
        #         else:
        #             child.opacity = 0

    def on_change_audio(self):
        if self.isStream is True:
            self.pipe.kill()
            self.prepare()