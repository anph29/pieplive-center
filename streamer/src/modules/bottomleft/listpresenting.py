import numpy as np
from kivy.uix.recycleview import RecycleView
from src.modules.recyclelayout.recyclegridlayout import SelectableGrid
from src.modules.recyclelayout.recyclegridlayout import SelectableBox
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
from src.modules.custom.popup import PiepMeConfirmPopup
from src.utils import helper, kivyhelper, firebase
from kivy.lang import Builder
from kivy.clock import Clock
from functools import partial

Builder.load_file('src/ui/listpresenting.kv')

class ListPresenting(RecycleView):

    def __init__(self, **kwargs):
        super(ListPresenting, self).__init__(**kwargs)

    def set_data(self):
        self.data = list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'],'active':False},
                helper._load_ls_presenter_action()
            )
        )

    def clean_data_to_save_json(self):
        return list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name']},
                list(self.data)
            )
        )

    def get_data(self):
        return self.data

    # def set_source(self,sources):
    #     self.data = sources

    def add_source(self, item):
        flag = False
        for _s in self.data:
            if _s['id'] == item['id']:
                flag = True
                break
        if flag == False:
            self.data.append(item)
            helper._write_lspresenter_action(self.clean_data_to_save_json())
    
    # def update_source(self, item):
    #     if self.data:
    #         for _s in self.data:
    #             if _s['id'] == item['id']:
    #                 _s.update(item)

    # def del_source(self, id):
    #     if self.data:
    #         for i,v in enumerate(self.data):
    #             if v['id'] == id:
    #                 del(self.data[i])

    def remove(self, index):
        if self.data:
            self.data.pop(index)
            helper._write_lspresenter_action(self.clean_data_to_save_json())

    def active_action(self, _id):
        for _s in self.data:
            if _s['id'] == _id:
                _s['active'] = True
        self.refresh_view()

    def deactive_action(self, _id):
        for _s in self.data:
            if _s['id'] == _id:
                _s['active'] = False
        self.refresh_view()
    
    def refresh_view(self):
        try:
            for child in self.children[0].children:
                child.refresh_view_attrs(self,child.index, self.data[child.index])
        except:
            pass
    
    def get_index_from_id(self, _id):
        for child in self.children[0].children:
            if child._id == _id:
                return child.index
        return -1

    # lay id tiep theo de auto choice play
    def get_next_id_from_id(self, _id):
        _idx = -1
        id = -1
        flag = False

        for child in self.children[0].children:
            if child._id == _id:
                _idx = child.index
                break
        if _idx != -1:
            for child in self.children[0].children:
                if child.index > _idx and child.active is True:
                    id = child._id
                    flag = True
            if flag is False:
                for child in self.children[0].children:
                    if int(child.index) < int(_idx) and child.active is True:
                        id = child._id
                        flag = True
        return id

    def get_number_active(self):
        num = 0
        for m in self.data:
            if m['active'] is True:
                num = num + 1
        return num
        

class BoxPresenting(SelectableBox):
    """ Adds selection and focus behaviour to the view. """

class RCVPresenting(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty(0)
    name = StringProperty('')
    active = BooleanProperty(False)
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.name = data['name']
        self._id = data['id']
        self.active = data['active']
        return super(RCVPresenting, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(RCVPresenting, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

    def open_confirm_rmv(self):
        PiepMeConfirmPopup(message='Are you sure to delete this resource?',
                               callback_ok=self.rmv_capture,
                               callback_cancel=lambda: True)

    def rmv_capture(self):
        self.parent.parent.remove(self.index)