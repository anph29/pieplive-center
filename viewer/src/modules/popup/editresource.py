import os
from src.utils import ftype, helper
import tkinter as tk
from tkinter import filedialog, ttk
from src.utils import tk_helper, scryto
from src.constants import UI
from src.constants.MTYPE import *
from src.enums import MediaType
from .addresource import PopupAddResource


class PopupEditResource(PopupAddResource):
    useLocal = False
    popup = None
    error = False

    def __init__(self, parent, data):
        self.parent = parent
        self.media = data

    def setupData(self):
        self.mtype = self.media["type"]
        self.duration = int(self.media["duration"]) if "duration" in self.media else 0
        self.id = self.media["id"]
        #
        name = self.media["name"]
        url = self.media["url"]
        self.name.set(name)
        self.url.set(url)

    def initGUI(self, data):
        # first destroy
        if None is not self.popup:
            self.popup.destroy()
        self.popup = tk_helper.makePiepMePopup(
            "Edit Media", w=450, h=200, padx=0, pady=0
        )
        self.initTabFileUI()

    def initTabFileUI(self):
        fFile = tk.Frame(self.popup)
        # var
        self.name = tk.StringVar()
        self.url = tk.StringVar()
        self.setupData()
        urlEditabel = self.mtype in [VIDEO, IMG]
        # name
        fName = tk.Frame(fFile, pady=10, padx=20)
        lName = tk.Label(fName, text="Name:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lName.pack(side=tk.LEFT, fill=tk.Y)
        self.eName = tk.Entry(
            fName, textvariable=self.name, width=100, borderwidth=5, relief=tk.FLAT
        )
        self.eName.pack(side=tk.LEFT, fill=tk.X)
        fName.pack(side=tk.TOP, fill=tk.X)
        # URL
        fUrl = tk.Frame(fFile, pady=10, padx=20)
        fUrl.pack(side=tk.TOP, fill=tk.X)
        lUrl = tk.Label(fUrl, text="URL:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lUrl.pack(side=tk.LEFT, fill=tk.Y)
        self.eUrl = tk.Entry(
            fUrl,
            textvariable=self.url,
            width=45 if urlEditabel else 100,
            borderwidth=5,
            relief=tk.FLAT,
            state=tk.NORMAL if urlEditabel else tk.DISABLED,
        )
        self.eUrl.pack(side=tk.LEFT, fill=tk.X)
        # btn Choose
        if urlEditabel:
            btnChoose = tk.Button(
                fUrl,
                text="Choose..",
                relief=tk.RAISED,
                padx=5,
                pady=5,
                command=self.askFileName,
                font=UI.TXT_FONT,
            )
            btnChoose.configure(width=7)
            btnChoose.pack(side=tk.RIGHT, fill=tk.Y)
        # duration
        if self.mtype in [VIDEO, M3U8]:
            self.packDuration(fFile)
        # error msg
        self.fError = tk.Frame(fFile)
        lError = tk.Label(self.fError, text="File not allowed!", fg="#f00")
        lError.pack(side=tk.LEFT, fill=tk.Y)

        # bot button
        fBtn = tk.Frame(fFile, pady=10, padx=20)
        btnCancel = tk.Button(
            fBtn, text="Cancel", bd=2, relief=tk.RAISED, command=self.popup.destroy
        )
        btnCancel.configure(width=7)
        btnCancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btnOk = tk.Button(
            fBtn,
            text="OK",
            bd=2,
            bg="#ff2d55",
            fg="#fff",
            relief=tk.RAISED,
            command=self.onSave,
        )
        btnOk.configure(width=7)
        btnOk.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        fBtn.pack(side=tk.BOTTOM, fill=tk.X)
        fFile.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def packDuration(self, wrapper):
        # var
        self.hh = tk.StringVar()
        self.hh.trace("w", self.limithh)
        self.mm = tk.StringVar()
        self.mm.trace("w", self.limitmm)
        self.ss = tk.StringVar()
        self.ss.trace("w", self.limitss)
        h, m, s = helper.convertSecNoToHMS(self.duration, toObj=True).values()
        # 2. Duration
        fDura = tk.Frame(wrapper, pady=10, padx=20)
        fDura.pack(side=tk.TOP, fill=tk.X)
        #
        lDura = tk.Label(
            fDura, text="Duration:", width=7, anchor=tk.W, font=UI.TXT_FONT
        )
        lDura.pack(side=tk.LEFT, fill=tk.Y)
        ##
        hh = ttk.Combobox(
            fDura,
            values=tk_helper.getComboboxValueRange(end=100),
            width=4,
            textvariable=self.hh,
            justify="right",
        )
        hh.bind("<FocusIn>", lambda args: hh.select_range("0", tk.END))
        hh.current(int(h))
        hh.pack(side=tk.LEFT, fill=tk.X, padx=5)
        ##
        separator = tk.Label(fDura, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=3)
        ##
        mm = ttk.Combobox(
            fDura,
            values=tk_helper.getComboboxValueRange(),
            width=4,
            textvariable=self.mm,
            justify="right",
        )
        mm.bind("<FocusIn>", lambda args: hh.select_range("0", tk.END))
        mm.current(int(m))
        mm.pack(side=tk.LEFT, fill=tk.X, padx=5)
        ##
        separator = tk.Label(fDura, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=3)
        ##
        ss = ttk.Combobox(
            fDura,
            values=tk_helper.getComboboxValueRange(),
            width=4,
            textvariable=self.ss,
            justify="right",
        )
        ss.bind("<FocusIn>", lambda args: ss.select_range("0", tk.END))
        ss.current(int(s))
        ss.pack(side=tk.LEFT, fill=tk.X, padx=5)

    def limithh(self, *arg):
        tk_helper.verifyHMS_val(self.hh)

    def limitmm(self, *arg):
        tk_helper.verifyHMS_val(self.mm)

    def limitss(self, *arg):
        tk_helper.verifyHMS_val(self.ss)

    def onSave(self):
        if self.mtype == VIDEO:
            self.duration = helper.convertHMSNoToSec(
                {
                    "h": int(self.hh.get()),
                    "m": int(self.mm.get()),
                    "s": int(self.ss.get()),
                }
            )

        self.parent.saveToMediaList(
            {
                "id": self.id,
                "name": self.name.get(),
                "url": self.url.get(),
                "type": self.mtype,
                "duration": self.duration,
            }
        )
        self.popup.destroy()
