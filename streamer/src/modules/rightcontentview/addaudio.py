from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from src.modules.custom.filechoose import FileChooser
from src.utils import ftype, helper, scryto
import src.utils.kivyhelper as kv_helper

Builder.load_file('src/ui/addaudio.kv')

class AddAudio(Popup):
    name = ObjectProperty()
    url = ObjectProperty()
    error = BooleanProperty(False)
    resource_type = ''
    use_local = False

    def __init__(self, parent):
        super(AddAudio, self).__init__()

    def add_to_lsaudio(self):
        helper._add_to_lsaudio({
            "id":scryto.hash_md5_with_time(self.url.text.replace('\\', '/')),
            "name": self.name.text,
            "url": self.url.text,
            "type": "AUDIO",
            'volume':100,
            'active': False
        })
        kv_helper.getApRoot().init_right_content_audio()
        self.dismiss()

    def on_ok(self):
        if self.use_local:
            self.add_to_lsaudio()
        elif len(self.url.text) > 0:
            self.resource_type = self.get_type_from_link()
            if self.resource_type:
                self.add_to_lsaudio()
            else:
                self.error = True
        else:
            self.error = True

    def on_cancel(self):
        self.dismiss()

    def open_file_browser(self):
        self.file_browser = FileChooser(self, self.choosed_file)
        self.file_browser.open()
        self.error = False

    def choosed_file(self, selection):
        if len(selection) == 1:
            if ftype.isAudio(selection[0]):
                self.local_file(selection[0], 'AUDIO')
            else:
                self.error = True

    def local_file(self, fpath, ftype):
        self.use_local = True
        self.resource_type = ftype
        self.url.text = fpath.replace('\\', '/')

    def get_type_from_link(self):
        URL = self.url.text.upper()
        if '.MP3' in URL or '.MID' in URL or '.WAV' in URL or '.M4A' in URL or '.OGG' in URL or '.FLAC' in URL or '.AMR' in URL:
            return 'AUDIO'
        else:
            return False
