import kivy
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder


class PiepMePopup(Popup):
    pass


"""
CONFIRM POPUP
"""
Builder.load_string('''
<PiepMeConfirmPopupContent>:
    cols:1
	Label:
		text: root.message
        halign: 'left'
        valign: 'middle'
        
    FloatLayout:
        size_hint: 1, None
		height: 50

	    BoxLayout:
            orientation: 'horizontal'
            size_hint: None, 1
            pos_hint:{'y':0, 'right':1}
            spacing:10
            width:230
            padding:10
            Button:
                text: 'OK'
                on_release: root.on_ok()
                width:100
            Button:
                text: 'Cancel'  
                on_release: root.on_cancel()
                width:100
''')


class PiepMeConfirmPopupContent(GridLayout):
    message = StringProperty()
    cb_ok = ObjectProperty()
    cb_cancel = ObjectProperty()

    def __init__(self, **kwargs):
        super(PiepMeConfirmPopupContent, self).__init__(**kwargs)

    def on_ok(self, *args):
        self.cb_ok()

    def on_cancel(self, *args):
        self.cb_cancel()


class PiepMeConfirmPopup():
    message = ''
    callback_ok = None
    callback_cancel = None

    def __init__(self, message, callback_ok, callback_cancel):
        self.message = message
        self.callback_ok = callback_ok
        self.callback_cancel = callback_cancel

        content = PiepMeConfirmPopupContent(
            message=self.message,
            cb_ok=self._on_ok,
            cb_cancel=self._on_cancel)

        self.popup = Popup(title="PiepMe",
                           content=content,
                           size_hint=(None, None),
                           size=(360, 180),
                           auto_dismiss=False)
        self.popup.open()

    def _on_ok(self, *args):
        self.callback_ok()
        self.popup.dismiss()

    def _on_cancel(self, *args):
        self.callback_cancel()
        self.popup.dismiss()


"""
END: CONFIRM POPUP
"""
