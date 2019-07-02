
from kivy.uix.recycleview import RecycleView
import src.utils.helper as helper
from kivy.properties import StringProperty

class ListMedia(RecycleView):
 
    def __init__(self, **kwargs):
        super(ListMedia, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_custom_resource()]

class ListCamera(RecycleView):

    def __init__(self, **kwargs):
        super(ListCamera, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_lscam()]


class ListPresenter(RecycleView):

    def __init__(self, **kwargs):
        super(ListPresenter, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_ls_presenter()]

class ListSchedule(RecycleView):

    def __init__(self, **kwargs):
        super(ListSchedule, self).__init__(**kwargs)

    def set_data(self):
        self.data = [c for c in helper._load_schedule()]
