import cv2
from kivy.uix.recycleview import RecycleView
import src.utils.helper as helper
from kivy.properties import StringProperty
from kivy.clock import Clock


class ListCamera(RecycleView):
    app_type = StringProperty()

    def __init__(self, **kwargs):
        super(ListCamera, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_lscam()]


class ListPresenter(RecycleView):
    app_type = StringProperty()

    def __init__(self, **kwargs):
        super(ListPresenter, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_ls_presenter()]

class ListSchedule(RecycleView):
    app_type = StringProperty()

    def __init__(self, **kwargs):
        super(ListSchedule, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_ls_schedule()]
