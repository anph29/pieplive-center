import tkinter as tk
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
        self.id = self.media['id'] if edit else scryto.hash_md5_with_time(self.url)
        self.eName = self.media['name'] if 'name' in self.media else ''
        self.url = self.media['url'] if 'url' in self.media else ''
        self.mtype = self.media['type'] if 'type' in self.media else ''
        self.duration = int(self.media['duration']) if 'duration' in self.media else 0
        self.timepoint = int(self.media['timepoint']) if 'timepoint' in self.media else 0
        self.audio = self.media['audio'] if 'audio' in self.media else ''
        #
    def setting_hms(self):
        self.name.set(self.eName)
        h,m,s = helper.convertSecNoToHMS(self.duration, toObj=True).values()
        self.hh.set(h)
        self.mm.set(m)
        self.ss.set(s)
        #
    def settingHMS(self):
        H,M,S = helper.convertSecNoToHMS(self.timepoint, toObj=True).values()
        self.HH.set(H)
        self.MM.set(M)
        self.SS.set(S)
        

    def initGUI(self, edit=False):
        # first destroy
        if bool(self.popup):
            self.popup.destroy()
        self.popup = tk_helper.makePiepMePopup('Add to Schedule', w=400, h=200, padx=0, pady=0)
        # var
        self.name = tk.StringVar()
        self.hh = tk.StringVar()
        self.hh.trace("w", self.limithh)
        self.mm = tk.StringVar()
        self.mm.trace("w", self.limitmm)
        self.ss = tk.StringVar()
        self.ss.trace("w", self.limitss)
        self.setupData(edit=edit)
        self.setting_hms()
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
        self.ehh = tk.Entry(fDura, textvariable=self.hh, width=4, borderwidth=5, relief=tk.FLAT, justify=tk.CENTER)
        self.ehh.bind("<FocusIn>", lambda args: self.ehh.select_range('0', tk.END))
        self.ehh.pack(side=tk.LEFT, fill=tk.X, padx=(10, 0))
        ##
        separator = tk.Label(fDura, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=5)
        ##
        self.emm = tk.Entry(fDura, textvariable=self.mm, width=4, borderwidth=5, relief=tk.FLAT, justify=tk.CENTER)
        self.emm.bind("<FocusIn>", lambda args: self.emm.select_range('0', tk.END))
        self.emm.pack(side=tk.LEFT, fill=tk.X)
        ##
        separator = tk.Label(fDura, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=5)
        ##
        lName.pack(side=tk.LEFT, fill=tk.Y)
        self.ess = tk.Entry(fDura, textvariable=self.ss, width=4, borderwidth=5, relief=tk.FLAT, justify=tk.CENTER)
        self.ess.bind("<FocusIn>", lambda args: self.ess.select_range('0', tk.END))
        self.ess.pack(side=tk.LEFT, fill=tk.X)
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
        self.popupRuntime = tk_helper.makePiepMePopup('Change runtime', w=300, h=180, padx=0, pady=0)
        # var
        self.HH = tk.StringVar()
        self.HH.trace("w", self.limitHH)
        self.MM = tk.StringVar()
        self.MM.trace("w", self.limitMM)
        self.SS = tk.StringVar()
        self.SS.trace("w", self.limitSS)
        self.setupData(edit=True)
        self.settingHMS()

        wrapper = tk.Frame(self.popupRuntime)
        wrapper.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # #0. timepoint
        fTime = tk.Frame(wrapper, pady=10, padx=20)
        fTime.pack(side=tk.TOP, fill=tk.X)
        #
        lTime = tk.Label(fTime, text="Runtime:", width=7, anchor=tk.W, font=UI.TXT_FONT)
        lTime.pack(side=tk.LEFT, fill=tk.Y)
        ##
        self.eHH = tk.Entry(fTime, textvariable=self.HH, width=4, borderwidth=5, relief=tk.FLAT, justify=tk.CENTER)
        self.eHH.bind("<FocusIn>", lambda args: self.eHH.select_range('0', tk.END))
        self.eHH.pack(side=tk.LEFT, fill=tk.X, padx=(10, 0))
        ##
        separator = tk.Label(fTime, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=5)
        ##
        self.eMM = tk.Entry(fTime, textvariable=self.MM, width=4, borderwidth=5, relief=tk.FLAT, justify=tk.CENTER)
        self.eMM.bind("<FocusIn>", lambda args: self.eMM.select_range('0', tk.END))
        self.eMM.pack(side=tk.LEFT, fill=tk.X)
        ##
        separator = tk.Label(fTime, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=5)
        ##
        self.eSS = tk.Entry(fTime, textvariable=self.SS, width=4, borderwidth=5, relief=tk.FLAT, justify=tk.CENTER)
        self.eSS.bind("<FocusIn>", lambda args: self.eSS.select_range('0', tk.END))
        self.eSS.pack(side=tk.LEFT, fill=tk.X)
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
            'duration': helper.convertHMSNoToSec({'h': self.hh.get(), 'm': self.mm.get(), 's': self.ss.get()}),
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
            'timepoint': helper.convertHMSNoToSec({'h': self.HH.get(), 'm': self.MM.get(), 's': self.SS.get()}),
            'audio':self.audio
        })
        self.popupRuntime.destroy()
