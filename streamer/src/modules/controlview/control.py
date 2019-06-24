from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty

Builder.load_file('src/ui/control.kv')
class Control(BoxLayout):
    btn_start = ObjectProperty()
    btn_record = ObjectProperty()
    btn_setting = ObjectProperty()
    