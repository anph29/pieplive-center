import tkinter as tk
from tkinter import ttk
from src.utils import tk_helper, helper, scryto
from src.constants import UI
import re

class PopupAddSchedule(object):

    def __init__(self, parent, data):
        self.popup = None
        self.popupRuntime = None
        self.parent = parent
        self.media = data
    
    def setupData(self, edit=False):
        self.url = self.media['url'] if 'url' in self.media else ''
        self.id = self.media['id'] if edit else scryto.hash_md5_with_time(self.url)
        self.eName = self.media['name'] if 'name' in self.media else ''
        self.mtype = self.media['type'] if 'type' in self.media else ''
        self.duration = int(self.media['duration']) if 'duration' in self.media else 0
        self.timepoint = int(self.media['timepoint']) if 'timepoint' in self.media else 0
        self.audio = self.media['audio'] if 'audio' in self.media else ''
        #

    def initGUI(self, edit=False):
        # first destroy
        if bool(self.popup):
            self.popup.destroy()
        self.popup = tk_helper.makePiepMePopup('Add to Schedule', w=400, h=200, padx=0, pady=0)
        # var
        self.hh = tk.StringVar()
        self.hh.trace("w", self.limithh)
        self.mm = tk.StringVar()
        self.mm.trace("w", self.limitmm)
        self.ss = tk.StringVar()
        self.ss.trace("w", self.limitss)
        self.setupData(edit=edit)
        self.name = tk.StringVar()
        self.name.set(self.eName)
        h,m,s = helper.convertSecNoToHMS(self.duration, toObj=True).values()
        #
        wrapper = tk.Frame(self.popup)
        wrapper.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #1. Name
        fName = tk.Frame(wrapper, pady=10, padx=20)
        lName = tk.Label(fName, text="Name:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lName.pack(side=tk.LEFT, fill=tk.Y)
        name = tk.Entry(fName, textvariable=self.name, width=100, borderwidth=5, relief=tk.FLAT)
        name.bind("<FocusIn>", lambda args: name.select_range('0', tk.END))
        name.pack(side=tk.LEFT, fill=tk.X, padx=(10, 0))
        fName.pack(side=tk.TOP, fill=tk.X)
        #2. Duration
        fDura = tk.Frame(wrapper, pady=10, padx=20)
        fDura.pack(side=tk.TOP, fill=tk.X)
        #
        lDura = tk.Label(fDura, text="Duration:", width=7, anchor=tk.W, font=UI.TXT_FONT)
        lDura.pack(side=tk.LEFT, fill=tk.Y)
        ##
        hh = ttk.Combobox(fDura, values=tk_helper.getComboboxValueRange(end=100), width=4, textvariable=self.hh, justify='right')
        hh.bind("<FocusIn>", lambda args: hh.select_range('0', tk.END))
        hh.current(h)
        hh.pack(side=tk.LEFT, fill=tk.X, padx=5)
        ##
        separator = tk.Label(fDura, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=3)
        ##
        mm = ttk.Combobox(fDura, values=tk_helper.getComboboxValueRange(), width=4, textvariable=self.mm, justify='right')
        mm.bind("<FocusIn>", lambda args: hh.select_range('0', tk.END))
        mm.current(m)
        mm.pack(side=tk.LEFT, fill=tk.X, padx=5)
        ##
        separator = tk.Label(fDura, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=3)
        ##
        ss = ttk.Combobox(fDura, values=tk_helper.getComboboxValueRange(), width=4, textvariable=self.ss, justify='right')
        ss.bind("<FocusIn>", lambda args: ss.select_range('0', tk.END))
        ss.current(s)
        ss.pack(side=tk.LEFT, fill=tk.X, padx=5)
        #4. Button
        fBtn = tk.Frame(wrapper, pady=10, padx=20)
        btnCancel = tk.Button(fBtn, text="Cancel", bd=2, relief=tk.RAISED, command=self.popup.destroy)
        btnCancel.configure(width=7)
        btnCancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btnOk = tk.Button(fBtn, text="OK", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.onSave)
        btnOk.configure(width=7)
        btnOk.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        fBtn.pack(side=tk.BOTTOM, fill=tk.X)

    def showChangeRuntimeUI(self):
        # first destroy
        if bool(self.popupRuntime):
            self.popupRuntime.destroy()
        self.popupRuntime = tk_helper.makePiepMePopup('Change runtime', w=300, h=120, padx=0, pady=0)
        # var
        self.HH = tk.StringVar()
        self.HH.trace("w", self.limitHH)
        self.MM = tk.StringVar()
        self.MM.trace("w", self.limitMM)
        self.SS = tk.StringVar()
        self.SS.trace("w", self.limitSS)
        self.setupData(edit=True)

        H,M,S = helper.convertSecNoToHMS(self.timepoint, toObj=True).values()
        wrapper = tk.Frame(self.popupRuntime)
        wrapper.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # #0. timepoint
        fTime = tk.Frame(wrapper, pady=20, padx=20)
        fTime.pack(side=tk.TOP, fill=tk.X)
        #
        lTime = tk.Label(fTime, text="Runtime:", width=7, anchor=tk.W, font=UI.TXT_FONT)
        lTime.pack(side=tk.LEFT, fill=tk.Y)
        ##
        HH = ttk.Combobox(fTime, values=tk_helper.getComboboxValueRange(end=100), textvariable=self.HH, width=4, justify='right')
        HH.bind("<FocusIn>", lambda args: HH.select_range('0', tk.END))
        HH.current(H)
        HH.pack(side=tk.LEFT, fill=tk.X, padx=5)
        ##
        separator = tk.Label(fTime, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=3)
        ##
        MM = ttk.Combobox(fTime, values=tk_helper.getComboboxValueRange(), width=4, textvariable=self.MM, justify='right')
        MM.bind("<FocusIn>", lambda args: MM.select_range('0', tk.END))
        MM.current(M)
        MM.pack(side=tk.LEFT, fill=tk.X, padx=5)
        ##
        separator = tk.Label(fTime, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=3)
        ##
        SS = ttk.Combobox(fTime, values=tk_helper.getComboboxValueRange(), width=4, textvariable=self.SS, justify='right')
        SS.bind("<FocusIn>", lambda args: SS.select_range('0', tk.END))
        SS.current(S)
        SS.pack(side=tk.LEFT, fill=tk.X, padx=5)
         #1. Button
        fBtn = tk.Frame(wrapper, pady=10, padx=20)
        btnCancel = tk.Button(fBtn, text="Cancel", bd=2, relief=tk.RAISED, command=self.popupRuntime.destroy)
        btnCancel.configure(width=7)
        btnCancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btnOk = tk.Button(fBtn, text="OK", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.onSaveRuntime)
        btnOk.configure(width=7)
        btnOk.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        fBtn.pack(side=tk.BOTTOM, fill=tk.X)

    def limithh(self, *arg):
       tk_helper.verifyHMS_val(self.hh)

    def limitmm(self, *arg):
       tk_helper.verifyHMS_val(self.mm)

    def limitss(self, *arg):
       tk_helper.verifyHMS_val(self.ss)

    def limitHH(self, *arg):
       tk_helper.verifyHMS_val(self.HH)

    def limitMM(self, *arg):
       tk_helper.verifyHMS_val(self.MM)

    def limitSS(self, *arg):
       tk_helper.verifyHMS_val(self.SS)

    def onSave(self):
        self.parent.saveToSchedule({
            'id':self.id,
            'name': self.name.get(), 
            'url': self.url, 
            'type': self.mtype,
            'duration': helper.convertHMSNoToSec({'h': int(self.hh.get()), 'm': int(self.mm.get()), 's': int(self.ss.get())}),
            'timepoint':self.timepoint,
            'audio':self.audio
        })
        self.popup.destroy()

    def onSaveRuntime(self):
        self.parent.calcRuntime({
            'id':self.id,
            'name': self.eName, 
            'url': self.url, 
            'type': self.mtype,
            'duration': self.duration,
            'timepoint': helper.convertHMSNoToSec({'h': int(self.HH.get()), 'm': int(self.MM.get()), 's': int(self.SS.get())}),
            'audio':self.audio
        })
        self.popupRuntime.destroy()
