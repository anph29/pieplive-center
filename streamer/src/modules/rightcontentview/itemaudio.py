from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from src.modules.custom.popup import PiepMeConfirmPopup
from kivy.lang import Builder
from src.utils import helper, kivyhelper
import datetime

Builder.load_file('src/ui/itemaudio.kv')
class ItemAudio(RecycleDataViewBehavior, FloatLayout):
    index = NumericProperty(0)
    dt_capture = ObjectProperty()
    name = StringProperty('')
    duration = NumericProperty()
    timepoint = NumericProperty()
    audio = StringProperty('')
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    isCheckItem = ObjectProperty()
    active = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        self.name = data['name']
        self.active = data['active']
        self.isCheckItem.active = False
        return super(ItemAudio, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(ItemAudio, self).on_touch_down(touch):
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
        if self.active is True:
            self.active = False
        else:
            self.active = True
        self.parent.parent.setActive(self.index,self.active)