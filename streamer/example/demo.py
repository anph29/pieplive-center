from functools import partial

import cv2

import datetime

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.graphics import Fbo, ClearColor, ClearBuffers, Scale, Translate
from kivy.clock import Clock
import subprocess

from kivy.properties import ObjectProperty

from kivy.config import Config
Config.set('graphics', 'width', 1280)
Config.set('graphics', 'height', 720)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '30')
Config.set('graphics', 'left', '20')
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'window_icon', 'src/images/logo.png')

Builder.load_string('''
<MyWidget>:
    btn:btn
    lbl:lbl
    kvcam:kvcam
    FloatLayout:
        id:kvcam
        size_hint: 1, 1
        pos_hint:{'x':0, 'y':0}
    Button:
        id:btn
        size_hint: 0.4, 0.2
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.5}
        on_press: root.click_me(args[0])
    Label:
        id:lbl
        color: 0,1,0,1
        font_size: 100
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.5}
        text: '...'
''')

#link play
#https://livevn.piepme.com/camhls/7421.36d74d5063fda77f18871dbb6c0ce613.m3u8
class MyWidget(FloatLayout):

    btn = ObjectProperty(None)
    lbl = ObjectProperty(None)
    kvcam = ObjectProperty(None)
    chcam = 0
    data={
        1:{
            'name':'anvideo',
            'url':'rtsp://viewer:FB1D2631C12FE8F7EE8951663A8A108@14.241.245.161:554',
            'capture': cv2.VideoCapture('rtsp://viewer:FB1D2631C12FE8F7EE8951663A8A108@14.241.245.161:554'),
            'type':'RTPS'
        },
        2:{
            'name':'anvideo',
            'url':'rtsp://viewer:FB1D2631C12FE8F7EE8951663A8A108@113.176.112.174:554',
            'capture': cv2.VideoCapture('rtsp://viewer:FB1D2631C12FE8F7EE8951663A8A108@113.176.112.174:554'),
            'type':'RTPS'
        },
        3:{
            'name':'anvideo',
            'url':'1.mp4',
            'capture': cv2.VideoCapture('1.mp4'),
            'type':'VIDEO'
        }
    }

    def __init__(self, *args, **kwargs):
        super(MyWidget, self).__init__(*args, **kwargs)
        print("inited!!!!")
        self.pipe = None
        self.lbl.text = "inited!!!!"
        Clock.schedule_interval(self.timer, 1)#0.03

    def timer(self, dt):
        now = datetime.datetime.now()
        self.lbl.text = now.strftime('%H:%M:%S')
        
    def click_me(self, button, *args):    
        # self.change_cam()
        if self.pipe is None:
            self.i = 0
            self.run_ffmpeg()
            self.run_anim(button)

    def run_ffmpeg(self, *args, **kwargs):
        command = ['../ffmpeg-win/ffmpeg.exe',
                '-thread_queue_size', '512',
                '-r', '30',
                '-f', 'rawvideo', 
                '-pix_fmt', 'rgba',
                '-s', '1280x720',
                '-i','-',
                '-stream_loop','-1', '-i','../../resource/media/muted.mp3',
                '-b:a', '128k',
                '-b:v', '1920k',
                '-g', '30', '-r', '30',
                '-threads', '2',
                '-f','flv',
                'rtmp://livevn.piepme.com/cam/7421.36d74d5063fda77f18871dbb6c0ce613?token=36d74d5063fda77f18871dbb6c0ce613&SRC=WEB&FO100=7421&PL300=8212&LN301=180&LV302=115.73.208.139&LV303=0982231325&LL348=1558771095036&UUID=247cbf2ee3f0bda1&NV124=vn&PN303=15&POS=3'
        ]
        self.pipe = subprocess.Popen(command, stdin=subprocess.PIPE)

    def release(self):
        if self.pipe is not None:
            self.pipe.kill()
        
    def run_anim(self, button, *args):
        anim = Animation(size_hint = (0.8, 0.4), duration=1.) + Animation(size_hint = (0.4, 0.2), duration=1.)
        anim.repeat = True
        anim.bind(on_progress=partial(self.save_frame, None))
        anim.start(button)

    def save_frame(self, textures, *args):
        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                self.parent.canvas.remove(self.canvas)
        fbo = Fbo(size=self.size, with_stencilbuffer=True)
        with fbo:
            ClearColor(0, 0, 0, 1)
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(-self.x, -self.y - self.height, 0)
        fbo.add(self.canvas)
        fbo.draw()
        self.pipe.stdin.write(fbo.pixels)
        fbo.remove(self.canvas)
        if self.parent is not None and canvas_parent_index > -1:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)
        return True
                

class MyApp(App):
    def build(self):        
        return MyWidget()

    def on_stop(self):
        App.get_running_app().root.release()

if __name__ == '__main__':
    MyApp().run()