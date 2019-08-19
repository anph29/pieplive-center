from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.filechooser import FileSystemLocal
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty

from src.modules.bottomleft.dropdownsource import DropDownSource
from src.modules.custom.mylabel import MyLabel
from src.modules.bottomleft.listmixer import ListMixer 
from src.modules.bottomleft.listmixer import BoxMixer 
from src.modules.bottomleft.listmixer import RCVItemMixer 
from src.modules.bottomleft.listsource import ListSource 
from src.modules.bottomleft.listsource import BoxSource 
from src.modules.bottomleft.listsource import RCVItemSource
from src.modules.bottomleft.listpresenting import ListPresenting 
from src.modules.bottomleft.listpresenting import BoxPresenting
from src.modules.bottomleft.listpresenting import RCVPresenting
from src.utils import ftype
from src.utils import kivyhelper as kv_helper
from src.modules.custom.filechoose import FileChooser

Builder.load_file('src/ui/bottomleft.kv')
class BottomLeft(GridLayout):

    def __init__(self, **kwargs):
        super(BottomLeft, self).__init__(**kwargs)
    
    def open_add_source(self, instance):
        dropdown = DropDownSource()
        dropdown.open(instance)

class TextDialog(Popup):
    inp_name = ObjectProperty()
    inp_text = ObjectProperty()
    inp_color = ObjectProperty()
    inp_font = ObjectProperty()
    inp_size = ObjectProperty()
    def __init__(self, parent, data = None, index = -1, *args):
        self.txt_color = 'ffffff'
        super(TextDialog, self).__init__(*args)
        self.fonts = ['Opensans', 'Roboto', 'AwkwardAlone', 'GoodBrush']
        self.index = index
        if data is not None:
            self.inp_name.text = data['name']
            self.inp_text.text = data['label']
            self.txt_color = data['color']
            self.inp_color._set_hex(data['color'])
            self.inp_font.text = data['font']
            self.inp_size.text = str(data['size'])
        self.inp_color.bind(color=self.on_color)

    def on_error(self, inst, text):
        pass

    def _enter(self):
        kv_helper.getApRoot().add_text(self.index,self.inp_name.text,self.inp_text.text,self.inp_font.text,self.inp_size.text,self.txt_color,0,0)
        self.dismiss()

    def _cancel(self):
        self.dismiss()

    def on_color(self,instance, value):
        self.txt_color = str(instance.hex_color)

class ImageDialog(Popup):
    directory = ''
    def __init__(self, parent, data = None, index = -1, *args):
        super(ImageDialog, self).__init__(*args)
        self.index = index
        if data is not None:
            self.inp_name.text = data['name']
            self.inp_source.text = data['src']
            self.inp_width.text = str(data['width'])
            self.inp_height.text = str(data['height'])

    def _enter(self):
        kv_helper.getApRoot().add_image(self.index, self.inp_name.text, self.inp_source.text, 0, 0, self.inp_width.text, self.inp_height.text)
        self.dismiss()

    def _cancel(self):
        self.dismiss()

    def choosed_file(self, selection):
        if len(selection) == 1:
            if ftype.isImage(selection[0]):
                self.local_file(selection[0], 'IMG')
            else:
                self.error = True

    def local_file(self, fpath, ftype):
        self.use_local = True
        self.resource_type = ftype
        self.inp_source.text = fpath.replace('\\', '/')

    def _choose_image(self):
        self.file_browser = FileChooser(self, self.choosed_file)
        self.file_browser.open()
        self.error = False
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def select(self, path):
        self.directory = path
        self.dismiss_popup()