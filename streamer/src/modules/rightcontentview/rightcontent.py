from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from src.modules.rightcontentview.addcamera import AddCamera
from src.modules.rightcontentview.addmedia import AddMedia
from src.modules.rightcontentview.addimage import AddImage
from src.modules.rightcontentview.addaudio import AddAudio
from src.modules.rightcontentview.itemlabel import ItemLabel
from src.modules.rightcontentview.itemschedule import ItemSchedule
from src.modules.rightcontentview.itempresenter import ItemPresenter
from src.modules.rightcontentview.itemaudio import ItemAudio
from src.utils import helper

Builder.load_file('src/ui/rightcontent.kv')

class RightContent(TabbedPanel):
    tab_media = ObjectProperty()
    tab_image = ObjectProperty()
    tab_audio = ObjectProperty()
    tab_camera = ObjectProperty()
    tab_presenter = ObjectProperty()
    tab_schedule = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(RightContent, self).__init__(*args, **kwargs)
        self.is_schedule = False
    
    def play_schedule(self, instance):
        if self.is_schedule == False:    
            self.is_schedule = True
            instance.source = helper._ICONS_PATH + 'pause.png'
        else:
            self.is_schedule = False
            instance.source = helper._ICONS_PATH + 'play-w.png'
        if self.f_parent is not None:
            self.f_parent.mainStream.start_schedule(self.is_schedule)
    
    def change_schedule_loop(self, _val):
        self.f_parent.mainStream.loop_schedule(_val)

class TabMedia(BoxLayout):
    add_media_pop = ObjectProperty()
    ls_media = ObjectProperty()

    def open_add_media(self):
        self.add_media_pop = AddMedia(self)
        self.add_media_pop.open()

class TabImage(BoxLayout):
    add_image_pop = ObjectProperty()
    ls_image = ObjectProperty()

    def open_add_image(self):
        self.add_image_pop = AddImage(self)
        self.add_image_pop.open()

class TabAudio(BoxLayout):
    add_audio_pop = ObjectProperty()
    ls_audio = ObjectProperty()

    def open_add_audio(self):
        self.add_audio_pop = AddAudio(self)
        self.add_audio_pop.open()

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
