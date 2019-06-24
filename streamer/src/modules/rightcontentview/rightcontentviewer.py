
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from src.modules.rightcontentview.controllers.addcamera import AddCamera
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('src/modules/rightcontentview/views/rightcontentviewer.kv')


class RightContentViewer(TabbedPanel):
    tab_camera = ObjectProperty()
    tab_presenter = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(RightContentViewer, self).__init__(*args, **kwargs)


class TabCameraViewer(BoxLayout):
    add_cam_pop = ObjectProperty()
    ls_camera = ObjectProperty()

    def open_add_camera(self):
        self.add_cam_pop = AddCamera(self)
        self.add_cam_pop.open()


class TabPresenterViewer(BoxLayout):
    add_presenter_pop = ObjectProperty()
    ls_presenter = ObjectProperty()

    def openAddPresenter(self):
        self.add_presenter_pop = AddCamera(self)
        self.add_presenter_pop.open()
