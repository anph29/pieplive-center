import kivy
import subprocess
import cv2
import numpy as np
import os
import src.utils.helper as helper
import time
from functools import partial
import multiprocessing
import sounddevice as sd
from threading import Thread, Event, ThreadError, Timer
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.graphics import Fbo, ClearColor, ClearBuffers, Scale, Translate
from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from src.modules.kvcam.kivycamera import KivyCamera
from src.modules.custom.pieplabel import PiepLabel
from src.modules.custom.piepimage import PiepImage

Clock.max_iteration = 60

class MainStream(RelativeLayout):

    def __init__(self, **kwargs):
        super(MainStream, self).__init__(**kwargs)
        self.f_width = 1280
        self.f_height = 720
        self.capture = None
        self.f_parent = None
        self.fps = 30
        self.v_bitrate = "1920k"
        self.urlStream = ''
        self.devAudio = None
        self.deviceVolume = 100
        self.isStream = False
        self.pipe = None
        self.lsSource = []
        self.command = []
        self.event = None

        self.mainView = RelativeLayout(size=(self.f_width, self.f_height))
        self.camera = KivyCamera(
            size=(self.f_width, self.f_height), pos=(0, 0))
        self.cameraView = KivyCamera(
            size=(self.f_width, self.f_height), pos=(0, 0))
        self.camera.idx = -1
        self.cameraView.idx = -1
        self.camera.f_height = self.f_height
        self.cameraView.f_height = self.f_height

        self.mainView.add_widget(self.camera)
        self.add_widget(self.cameraView)

    def _set_capture(self, data_src):
        self.camera.set_data_source(data_src)
        self.cameraView.set_data_source(data_src)

    def is_streaming(self):
        return self.isStream

    def startStream(self):
        print("--- START ---")
        self.fbo = Fbo(size=(self.f_width, self.f_height),
                       with_stencilbuffer=True)
        with self.fbo:
            ClearColor(0, 0, 0, 1)
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(-self.mainView.x, -self.mainView.y -
                      self.mainView.height, 0)
        self.fbo.add(self.mainView.canvas)
        self.isStream = True
        self.event = Clock.schedule_interval(self.stream, 1/60)
   
    @mainthread
    def stream(self, fps,*args):
        try:
            if self.isStream:
                self.fbo.draw()
                self.pipe.stdin.write(self.fbo.pixels)
        except IOError:
            #helper.getApRoot().triggerStop()
            self.pipe.kill()
            self.fbo.remove(self.mainView.canvas)
            if self.event is not None:
                self.event.cancel()

    def set_url_stream(self, urlStream):
        self.urlStream = urlStream

    def set_device_audio(self, devAudio):
        self.devAudio = devAudio

    def draw_element(self):
        numau = 0
        inp = []
        txt2 = ''
        if self.devAudio is not None:
            numau = 1
            txt2 += "volume={},".format(self.deviceVolume/100)
        if len(self.lsSource) > 0:
            for value in self.lsSource:
                if value['active'] == 1:
                    if(value['type'] == 'audio'):
                        inp.extend(["-i", value['src']])
                        txt2 += 'volume={},'.format(str(value['volume']/100))
                        numau += 1
            if numau > 0:
                txt2 += 'amix=inputs={}'.format(str(numau))
            if len(txt2) > 0:
                inp.extend(['-filter_complex', txt2])
        return inp

    def prepare(self):
        try:
            print('asd bubub')
            self.command = ['ffmpeg-win/ffmpeg.exe','-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '{}x{}'.format(self.f_width, self.f_height), '-i', '-']
            # audio
            if self.devAudio is not None:
                self.command.extend(
                    ['-f', 'dshow', '-i', 'audio={}'.format(self.devAudio)])

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
        self.fbo.remove(self.mainView.canvas)
        print("--- STOP ---")

    def release(self):
        if self.event is not None:
            self.event.cancel()
        if self.pipe is not None:
            self.pipe.kill()
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
        for child in self.mainView.children:
            if child.idx == idx:
                child.x = pos_x
                child.top = pos_y
                break

    def show_text(self, text, font, size, color, pos_x, pos_y, active, idx):
        pText2 = PiepLabel(text='[color=' + str(color) + ']' + text + '[/color]',
                           font_size=size,
                           font_name=font,
                           x=pos_x,
                           top=pos_y,
                           markup=True,
                           opacity=active,
                           idx=idx,
                           parentName='main')
        pText = PiepLabel(text='[color=' + str(color) + ']' + text + '[/color]',
                          font_size=size,
                          font_name=font,
                          x=pos_x,
                          top=pos_y,
                          opacity=active,
                          markup=True,
                          idx=idx,
                          parentName='canvas')
        self.add_widget(pText2)
        self.mainView.add_widget(pText)

    def show_image(self, src, pos_x, pos_y, w, h, active, idx):
        pimage2 = PiepImage(source=src,
                            size=(w, h),
                            x=pos_x,
                            top=pos_y,
                            opacity=active,
                            idx=idx,
                            parentName='main')

        pimage = PiepImage(source=src,
                           size=(w, h),
                           x=pos_x,
                           top=pos_y,
                           opacity=active,
                           idx=idx,
                           parentName='canvas')
        self.add_widget(pimage2)
        self.mainView.add_widget(pimage)

    def on_off_source(self, idx, value):
        for child in self.children:
            if child.idx != None and child.idx == idx:
                if value:
                    child.opacity = 1
                else:
                    child.opacity = 0
        for child in self.mainView.children:
            if child.idx == idx:
                if value:
                    child.opacity = 1
                else:
                    child.opacity = 0
