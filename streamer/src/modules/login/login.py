from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty, ObjectProperty
from src.utils import helper
from src.utils import socket_client
from kivy.clock import Clock

Builder.load_file('src/modules/login/login.kv')


class Login(Popup):
    token_expired = BooleanProperty(False)
    qr_login = ObjectProperty()

    def __init__(self, parent):
        super(Login, self).__init__()

    def open(self):
        super(Login, self).open()
        Clock.schedule_once(lambda x: socket_client.open(), 1)

    def refresh_token(self):
        Clock.schedule_once(30.0, lambda x: self.let_expire())

    def let_expire(self):
        pass

    def _cancel(self):
        self.dismiss()
