from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from src.utils import kivyhelper as kv_helper
from src.utils import helper as helper

class ScheduleManager(Widget):
    
    videoBuffer = ObjectProperty()

    def __init__(self, **kwargs):
        super(ScheduleManager, self).__init__(**kwargs)

    def start(self):
        