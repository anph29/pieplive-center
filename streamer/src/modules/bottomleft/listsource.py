from kivy.uix.recycleview import RecycleView
from src.modules.recyclelayout.recyclegridlayout import SelectableGrid
from src.modules.recyclelayout.recyclegridlayout import SelectableBox
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from src.modules.custom.popup import PiepMeConfirmPopup
from src.utils import kivyhelper

Builder.load_file('src/ui/listsource.kv')

class ListSource(RecycleView):
    list_source = ObjectProperty()

    def __init__(self, **kwargs):
        super(ListSource, self).__init__(**kwargs)
        self.data = []
        
    def set_source(self,sources):
        self.data = []
        if sources is not None:
            for i in sources:
                self.data.append({"name":i["name"], "active": i["active"]})

    def add_source(self, item):
        self.data.append({"name":item["name"], "active": item["active"]})

    def update_source(self, pos, item):
        self.data[pos].update(item)

    def del_source(self, pos):
        del(self.data[pos])

    def confirmDelete(self):
        PiepMeConfirmPopup(message='Are you sure to delete this source?',
                        callback_ok=self.delete_source,
                        callback_cancel=lambda: True)

    def delete_source(self):
        for child in self.children[0].children:
            if child.selected:
                kivyhelper.getApRoot().delete_source(child.index)
                del(self.data[child.index])
    
    def on_change_check(self, index, active):
        if self.data[index]['active'] == 1:
            self.data[index]['active'] = 0
        elif self.data[index]['active'] == 0:
            self.data[index]['active'] = 1

    def edit_source(self):
        for child in self.children[0].children:
            if child.selected:
                kivyhelper.getApRoot().on_edit_source(child.index)

class BoxSource(SelectableBox):
    """ Adds selection and focus behaviour to the view. """
    selected_source = StringProperty()


class RCVItemSource(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty(0)
    active = NumericProperty(0)
    name = StringProperty()
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.name = data['name']
        self.active = data['active']
        return super(RCVItemSource, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(RCVItemSource, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
    
    def on_change_check(self):
        if self.active == 1:
            self.active = 0
        elif self.active == 0:
            self.active = 1
        self.parent.parent.on_change_check(self.index,self.active)
        kivyhelper.getApRoot().on_off_source(self.index,self.active)