import tkinter as tk
import PIL
from PIL import Image, ImageTk
from src.utils import helper, tk_helper, store
import re
from src.models.n100_model import N100_model
from uuid import getnode as get_mac
from src.utils import store
from tkinter import messagebox
from src.constants import WS, UI
import time

class Login(object):
    loginPopup = None

    def __init__(self, parent):
        self.parent = parent
        super(Login, self).__init__()
    
    def logout(self):
        if messagebox.askyesno("PiepMe", "Are you sure to logout?"):
            # clear store
            store._new({})
            # clear resource 
            self.parent.tab_camera.clearData()
            self.parent.tab_presenter.clearData()
            #
            self.parent.hideToolbar()
            self.open()

    def open(self):
         # first destroy
        if None is not self.loginPopup:
            self.loginPopup.destroy()
        # init
        self.loginPopup = tk_helper.makePiepMePopup("Login", w=500, h=400)
        # var
        self.NV117 = tk.StringVar()
        self.PV161 = tk.StringVar()
        #
        loginMainFrame = tk.Frame(self.loginPopup, pady=50)
        loginMainFrame.pack()
        # logo
        fLogo = tk.Frame(loginMainFrame, pady=10)
        fLogo.pack()
        imgLogo = ImageTk.PhotoImage(Image.open(helper._LOGO_VIEWER))
        lblLogo = tk.Label(fLogo, image=imgLogo, bg="#f2f2f2")
        lblLogo.photo = imgLogo
        lblLogo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # PiepMe ID
        self.fPid = tk.Frame(loginMainFrame, pady=15)
        self.fPid.pack()
        ePid = tk.Entry(self.fPid, textvariable=self.NV117, borderwidth=5, relief=tk.FLAT)
        ePid.insert(0, 'GP2Y6B')  # 'PiepMe ID')
        ePid.bind("<FocusIn>", lambda args: ePid.delete('0', 'end'))
        ePid.config(font=UI.TXT_FONT)
        self.NV117.trace("w", self.autoUpperNV117)
        ePid.pack(side=tk.LEFT, fill=tk.X)
        #
        btnLogin = tk.Button(self.fPid, text="Login", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.onSendNV117)
        btnLogin.config(width=7, font=UI.TXT_FONT)
        btnLogin.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        # Verify TOKEN
        self.fToken = tk.Frame(loginMainFrame, pady=15)
        eToken = tk.Entry(self.fToken, textvariable=self.PV161, borderwidth=5, relief=tk.FLAT)
        eToken.insert(0, 'Token')
        eToken.bind("<FocusIn>", lambda args: eToken.delete('0', 'end'))
        eToken.config(font=UI.TXT_FONT)
        eToken.pack(side=tk.LEFT, fill=tk.X)
        #
        btnVerify = tk.Button(self.fToken, text="Verify", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.onVerify)
        btnVerify.config(width=7, font=UI.TXT_FONT)
        btnVerify.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        #
        lblCommand = tk.Label(self.fToken, text="Check your PiepMe message to get verify token!")
        btnVerify.config(font=UI.TXT_FONT)
        btnVerify.pack()
        # nv117 invalid
        self.fInvalid = tk.Frame(loginMainFrame, pady=5)
        lblError = tk.Label(self.fInvalid, text="PiepMe ID invalid!", fg="#f00")
        lblError.config(font=UI.TXT_FONT)
        lblError.pack(side=tk.LEFT, fill=tk.Y)
        # pv161 invalid
        self.fTokenInvalid = tk.Frame(loginMainFrame, pady=5)
        lblTOkenError = tk.Label(self.fTokenInvalid, text="Token invalid!", fg="#f00")
        lblTOkenError.config(font=UI.TXT_FONT)
        lblTOkenError.pack(side=tk.LEFT, fill=tk.Y)


    def autoUpperNV117(self, *arg):
        self.NV117.set(self.NV117.get().upper())
        tk_helper.character_limit(self.NV117)

    def onSendNV117(self):
        self.fInvalid.pack_forget()
        regex = re.compile(r"^[A-Z0-9]{6,8}$")
        nv117 = self.NV117.get()
        if regex.match(nv117):
            res = self.getOtpViaNV117(nv117)
            if res[WS.STATUS] == WS.SUCCESS:
                self.fPid.pack_forget()
                self.fToken.pack(side=tk.LEFT, fill=tk.X)
            else:
                self.fInvalid.pack(side=tk.LEFT, fill=tk.Y)
        else:
            self.fInvalid.pack(side=tk.LEFT, fill=tk.Y)

    def onVerify(self):
        self.fTokenInvalid.pack_forget()
        regex = re.compile(r"^[0-9]{6}$")
        pv161 = self.PV161.get()
        if regex.match(pv161):
            res = self.pieplivecenterLogin(self.NV117.get(), pv161)
            print(res, 'loginggggg')
            if res[WS.STATUS] == WS.SUCCESS and res[WS.ELEMENTS] != -1:
                # save login
                store._new(res[WS.ELEMENTS])
                #
                self.parent.showToolbar()
                self.loginPopup.destroy()

            else:
                self.fTokenInvalid.pack(side=tk.LEFT, fill=tk.Y)
        else:
            self.fTokenInvalid.pack(side=tk.LEFT, fill=tk.Y)

    def getOtpViaNV117(self, nv117):
        n100 = N100_model()
        return n100.getOtpViaNV117({
            'NV117': nv117,  # PiepMeID
            'LOGIN': hex(get_mac())  # IP hoặc Mac address (của máy)
        })

    def pieplivecenterLogin(self, nv117, pv161):
        n100 = N100_model()
        return n100.pieplivecenterLogin({
            'NV117': nv117,  # PiepMeID
            'PV161': pv161,  # OTP (login)
            'LOGIN': hex(get_mac())  # IP hoặc Mac address (của máy)
        })
