from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ObjectProperty, NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from src.modules.custom.popup import PiepMeConfirmPopup
from src.modules.kvcam.labelcamera import LabelCamera
from kivy.lang import Builder
from src.utils import kivyhelper as kv_helper
from src.modules.custom.addschedule import AddSchedule

Builder.load_file('src/ui/itemlabel.kv')
class ItemLabel(RecycleDataViewBehavior, FloatLayout):
    index = NumericProperty(0)
    dt_capture = ObjectProperty()
    name = StringProperty('')
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    kvcam = ObjectProperty()
    isCheckItem = ObjectProperty()
    active = BooleanProperty(False)
    choice = BooleanProperty(False)
    playable = BooleanProperty(False)
    duration = NumericProperty(0)
    listType = StringProperty('')
    _id = StringProperty('')
    showMiniD = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.is_changing = False
        self.index = index
        self.name = data['name']
        self._id = data['id']
        self.kvcam.set_data_source(data)
        self.duration = data['duration'] if 'duration' in data else 0
        self.listType = data['list']
        self.data = data
        self.active = data['active']
        self.choice = data['choice']
        self.playable = data['playable'] if 'playable' in data else True
        self.isCheckItem.active = False
        return super(ItemLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(ItemLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view """
        self.selected = is_selected

    def open_confirm_rmv(self):
        PiepMeConfirmPopup(message='Are you sure to delete this resource?',
                               callback_ok=self.rmv_capture,
                               callback_cancel=lambda: True)

    def rmv_capture(self):
        self.parent.parent.remove(self.index)

    def add_to_schedule(self):
        kv_helper.getApRoot().open_add_schedule(self.data)
    
    def play(self):
        if self.playable:
            self.isCheckItem.active = False
            self.parent.parent.setPlayed(self.index)
            kv_helper.getApRoot().changeSrc(self.kvcam.get_data_source(),self.listType)
    
    def playMini(self, isPlay):
        if self.playable and isPlay:
            kv_helper.getApRoot().changeSrcMini(self.kvcam.get_data_source(),self.listType)

    def choice_play(self):
        if self.listType == 'PRESENTER':
            self.parent.parent.choice_play(self.index)