from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.dropdown import DropDown
import src.utils.helper as helper
from kivy.lang import Builder

from kivy.lang import Builder
from functools import partial

kv = '''
<DropDownSource>:
    canvas.before:
        Color:
            rgb: .21,.21,.21
        Rectangle:
            pos: self.pos
            size: self.size
    MyLabel:
        text: 'Image'
        size_hint_x:1
        size_hint_y: None
        font_size: sp(14)
        height: 28
        text_size:self.size
        on_release: app.root.add_source("IMAGE")
        halign:"justify"
        valign:"middle"
    MyLabel:
        text: 'Text'
        size_hint_y: None
        font_size: sp(14)
        height: 30
        text_size:self.size
        on_release: app.root.add_source('TEXT')
        halign:"justify"
        valign:"middle"
    MyLabel:
        text: 'Audio'
        size_hint_y: None
        font_size: sp(13)
        height: 26
        text_size:self.size
        on_release: app.root.add_source('AUDIO')
        halign:"justify"
        valign:"middle"
'''

Builder.load_string(kv)

class DropDownSource(DropDown):
    pass