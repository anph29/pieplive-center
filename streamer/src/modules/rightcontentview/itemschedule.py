from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ObjectProperty, NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from src.modules.custom.popup import PiepMeConfirmPopup
from src.modules.kvcam.labelcamera import LabelCamera
from kivy.lang import Builder
from src.utils import kivyhelper as kvhelper
from src.utils import helper
import datetime

Builder.load_file('src/ui/itemschedule.kv')
class ItemSchedule(RecycleDataViewBehavior, FloatLayout):
    index = NumericProperty(0)
    dt_capture = ObjectProperty()
    name = StringProperty()
    duration = NumericProperty()
    timepoint = NumericProperty()
    audio = StringProperty()
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    kvcam = ObjectProperty()
    isCheckItem = ObjectProperty()
    active = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        self.name = data['name']
        self.duration = data['duration']
        self.timepoint = data['timepoint']
        self.audio = data['audio']
        self.kvcam.set_data_source(data)
        self.active = data['active']
        self.isCheckItem.active = False
        return super(ItemSchedule, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(ItemSchedule, self).on_touch_down(touch):
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

    def play(self):
        self.isCheckItem.active = False
        self.parent.parent.setPlayed(self.index)
        kvhelper.getApRoot().changeSrc(self.kvcam.get_data_source(),'SCHEDULE')
        self.parent.parent.makeTimePoint(self.index)

    def up(self):
        self.parent.parent.up_list(self.index)

    def down(self):
        self.parent.parent.down_list(self.index)

    def viewTimePoint(self,_second):
        h,m,s = helper.convertSecNoToHMS(_second, toObj=True).values()
        return f'{h}h {m}:{s}'

    def link_audio(self, obj):
        self.parent.parent.link_audio(obj, self.index,self.audio)