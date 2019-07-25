import sys
from os.path import sep, expanduser, dirname
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.garden.filebrowser import FileBrowser
from kivy.lang import Builder

Builder.load_string('''
<FileChooser>:
    title: 'Choose File..'
    color:1,0,0,1
    size_hint:None, None
    width:sp(900)
    height:sp(650)
    auto_dismiss: False
    padding:0
''')

class FileChooser(Popup):
    callback = None

    def __init__(self, parent, cb):
        super(FileChooser, self).__init__()

        self.callback = cb

        if sys.platform == 'win':
            user_path = dirname(expanduser('~')) + sep + 'Documents'
        else:
            user_path = expanduser('~') + sep + 'Documents'

        browser = FileBrowser(select_string='Select', favorites=[
                              (user_path, 'Documents')])
        browser.bind(on_success=self._fbrowser_success,
                     on_canceled=self._fbrowser_canceled,
                     on_submit=self._fbrowser_submit)

        self.add_widget(browser)

    def _fbrowser_canceled(self, instance):
        self.dismiss()

    def _fbrowser_success(self, instance):  # select pressed
        self.callback(instance.selection)
        self.dismiss()

    def _fbrowser_submit(self, instance):  # clicked on the file
        self.callback(instance.selection)
        self.dismiss()
