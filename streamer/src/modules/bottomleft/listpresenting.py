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

Builder.load_file('src/ui/listpresenting.kv')

class ListPresenting(RecycleView):

    def __init__(self, **kwargs):
        super(ListPresenting, self).__init__(**kwargs)

    def set_source(self,sources):
        self.data = sources

    def add_source(self, item):
        flag = False
        for _s in self.data:
            if _s['id'] == item['id']:
                flag = True
                break
        if flag == False:
            self.data.append(item)
    
    def update_source(self, item):
        for _s in self.data:
            if _s['id'] == item['id']:
                _s.update(item)

    def del_source(self, id):
        for i,v in enumerate(self.data):
            if v['id'] == id:
                del(self.data[i])

class BoxPresenting(SelectableBox):
    """ Adds selection and focus behaviour to the view. """

class RCVPresenting(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty(0)
    name = StringProperty('')
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.name = data['name']
        self._id = data['id']
        return super(RCVPresenting, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(RCVPresenting, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected