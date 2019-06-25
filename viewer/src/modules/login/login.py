from src.utils import helper
from src.utils import socket_client
import tkinter as tk
from src.utils import tk_helper
from PIL import Image, ImageTk


class Login(object):
    loginPopup = None

    def __init__(self, parent):
        super(Login, self).__init__()

    def open(self):
         # first destroy
        if None is not self.loginPopup:
            self.loginPopup.destroy()
        # init
        self.loginPopup = tk_helper.makePiepMePopup("Login", "400x250+400+300")
        # var
        self.qrCode = tk.StringVar()
        self.tokenExpired = tk.BooleanVar(False)
        # logo
        wLogo = tk.Frame(self,  relief=tk.FLAT, bg='#fff', borderwidth=5)
        pmLogo = ImageTk.PhotoImage(Image.open("../resource/icons/logo-viewer.png"))
        lblLogo = tk.Label(wLogo, image=pmLogo, bg="#f2f2f2")
        lblLogo.image = pmLogo
        # qr-Code holder
        # label

        # Clock.schedule_once(lambda x: socket_client.open(), 1)

    def refresh_token(self):
        # Clock.schedule_once(30.0, lambda x: self.let_expire())
        pass

    def let_expire(self):
        pass
