import kivy
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from os import listdir, path

Builder.load_string('''
<ChooseFile>:
    canvas.before:
        Color:
            rgba: 0, 0, .4, 1
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserIconView:
            id: filechooser
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                background_color: 0,.5,1,1
                on_release: root.cancel()
            Button:
                text: "Select Folder"
                background_color: 0,.5,1,1
                on_release: root.select(filechooser.path)
''')

class ChooseFile(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)