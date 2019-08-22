import cv2, subprocess
import numpy as np

import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
import ffpyplayer
from ffpyplayer.player import MediaPlayer
import time




kv ='''
<MyWidget>:
    id:mainView
    size_hint:1,1
    Button:
        id:btn_start
        size_hint:None,None
        width:120
        text:'Start'
        font_size: sp(12)
        on_press: root.playff()

'''
Builder.load_string(kv)

class MyWidget(BoxLayout):
    mainView = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(MyWidget, self).__init__(*args, **kwargs)

    def playff(self):
        video_path="C:/Users/Thong/Desktop/piep-source/videos/anh-thuong-em-nhat-ma-30.mp4"

        player = MediaPlayer(video_path)
        val = ''
        while val != 'eof':
            frame, val = player.get_frame()
            if val != 'eof' and frame is not None:
                img, t = frame

class TestApp(App):
    
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    TestApp().run()