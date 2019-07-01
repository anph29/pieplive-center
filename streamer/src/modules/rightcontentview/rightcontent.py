
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from src.modules.rightcontentview.addcamera import AddCamera
from src.modules.rightcontentview.itemlabel import ItemLabel
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('src/ui/rightcontent.kv')

class RightContent(TabbedPanel):
    tab_camera = ObjectProperty()
    tab_presenter = ObjectProperty()
    tab_schedule = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(RightContent, self).__init__(*args, **kwargs)


class TabCamera(BoxLayout):
    add_cam_pop = ObjectProperty()
    ls_camera = ObjectProperty()

    def open_add_camera(self):
        self.add_cam_pop = AddCamera(self)
        self.add_cam_pop.open()

class TabPresenter(BoxLayout):
    add_presenter_pop = ObjectProperty()
    ls_presenter = ObjectProperty()

    def openAddPresenter(self):
        self.add_presenter_pop = AddCamera(self)
        self.add_presenter_pop.open()

class TabSchedule(BoxLayout):
    add_schedule_pop = ObjectProperty()
    ls_schedule = ObjectProperty()

    def openAddSchedule(self):
        self.add_schedule_pop = AddCamera(self)
        self.add_schedule_pop.open()
