import kivy
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.uix.popup import Popup
from src.modules.custom.filechoose import FileChooser
from kivy.uix.recycleview import RecycleView
from src.modules.recyclelayout.recyclegridlayout import SelectableBox
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from src.utils import ftype, helper, scryto

Builder.load_file('src/ui/linkaudio.kv')

class LinkAudio(Popup):
    rcv_audio = ObjectProperty()
    callback = ObjectProperty()
    lsAudio = []

    def __init__(self, parent, idx, src, callback):
        super(LinkAudio, self).__init__()
        self.idx = idx
        self.callback = callback
        self.lsAudio = []
        self.lsAudio = list(
            map(
                lambda cam: {'id': cam['id'],'name': cam['name'], 'url': cam['url'],
                'active':True if cam['url'] == src else False},
                helper._load_ls_audio()
            )
        )
        self.rcv_audio.set_source(self.lsAudio)

    def on_ok(self):
        try:
            idx = self.rcv_audio.getIndexOfSeleced()
            if idx != -1:
                src = self.lsAudio[idx]['url']
                self.callback(src, self.idx)
                self.dismiss()
        except:
            pass
            
    def on_remove(self):
        self.callback('', self.idx)
        self.dismiss()

    def on_cancel(self):
        self.dismiss()


class ListAudio(RecycleView):
    list_source = ObjectProperty()

    def __init__(self, **kwargs):
        super(ListAudio, self).__init__(**kwargs)
        self.data = []
        
    def set_source(self,sources):
        self.data = sources

    def getIndexOfSeleced(self):
        for child in self.children[0].children:
            if child.active:
                return child.index
        return -1
    
    def set_active(self,index):
        for obj in self.data:
            obj['active'] = False
        self.data[index]['active'] = True
        for child in self.children[0].children:
            if child.index == index:
                child.active = True
            else:
                child.active = False

class BoxAudio(SelectableBox):
    """ Adds selection and focus behaviour to the view. """
    selected_source = StringProperty()


class RCVAudio(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty(0)
    name = StringProperty()
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    active = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.name = data['name']
        self.active = data['active']
        return super(RCVAudio, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(RCVAudio, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

    def set_active(self):
        self.parent.parent.set_active(self.index)