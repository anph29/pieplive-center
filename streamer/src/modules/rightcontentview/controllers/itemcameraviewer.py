from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ObjectProperty, NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from src.modules.custom.popup import PiepMeConfirmPopup
from kivy.lang import Builder
from src.utils import helper


Builder.load_file('src/modules/rightcontentview/views/itemcameraviewer.kv')
class ItemCameraViewer(RecycleDataViewBehavior, FloatLayout):
    index = NumericProperty(0)
    dt_capture = ObjectProperty()
    name = StringProperty()
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    kvcam = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        self.name = data['name']
        self.kvcam.set_data_source(data)
        return super(ItemCameraViewer, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(ItemCameraViewer, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view """
        self.selected = is_selected
        if self.selected:
            helper.getApRoot().changeSrc(self.kvcam.get_data_source())

    def open_confirm_rmv(self):
        if not self.selected:
            PiepMeConfirmPopup(message='Are you sure to delete this resource?',
                               callback_ok=self.rmv_capture,
                               callback_cancel=lambda: True)

    def rmv_capture(self):
        self.kvcam.capture.release()
        self.parent.remove(self.index)
