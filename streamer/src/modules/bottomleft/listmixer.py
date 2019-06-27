import numpy as np
from kivy.uix.recycleview import RecycleView
from src.modules.recyclelayout.recyclegridlayout import SelectableGrid
from src.modules.recyclelayout.recyclegridlayout import SelectableBox
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
import src.utils.kivyhelper as kv_helper
from kivy.lang import Builder
from kivy.clock import Clock
from functools import partial

Builder.load_file('src/ui/listmixer.kv')

class ListMixer(RecycleView):

    def __init__(self, **kwargs):
        super(ListMixer, self).__init__(**kwargs)

    def set_source(self,sources):
        self.data = sources

    def add_source(self, item):
        flag = False
        for _s in self.data:
            if _s['idx'] == item['idx']:
                flag = True
                break
        if flag == False:
            self.data.append(item)
    
    def update_source(self, item):
        for _s in self.data:
            if _s['idx'] == item['idx']:
                _s.update(item)

    def del_source(self, idx):
        for i,v in enumerate(self.data):
            if v['idx'] == idx:
                del(self.data[i])

    def on_start(self):
        print("start")


class BoxMixer(SelectableBox):
    """ Adds selection and focus behaviour to the view. """


class RCVItemMixer(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty(0)
    volume = NumericProperty(0)
    value = StringProperty()
    name = StringProperty()
    audio_volume = ObjectProperty()
    audio_status = ObjectProperty()
    clock = ObjectProperty()
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    duration = 1

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.name = data['name']
        self.value = data['value']
        self.volume = data['volume']
        self.idx = data['idx']
        # if self.idx == -1:
        #     self.event = Clock.schedule_interval(self.real_audio, 1)
        return super(RCVItemMixer, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(RCVItemMixer, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

    def onChangeVolume(self, value):
        if self.clock is not None:
            self.clock.cancel()
        self.clock = Clock.schedule_once(lambda x:kv_helper.getApRoot().changeAudioVolume(self.idx, self.audio_volume.value), 1)

    def print_sound(self,indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata)*100
        self.audio_status.value=volume_norm

    def real_audio(self, dt):
        #aa = sd.Stream(callback=self.print_sound)
        pass