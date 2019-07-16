import tkinter as tk
from src.utils import tk_helper, helper, scryto
from src.constants import UI
import re

class PopupAddSchedule(object):
    popup = None

    def __init__(self, parent, data):
        self.parent = parent
        self.media = data
    
    def setupData(self):
        self.url = self.media['url']
        self.mtype = self.media['type']
        self.duration = int(self.media['duration']) if 'duration' in self.media else 0
        self.id = scryto.hash_md5_with_time(self.url)
        #
        name = self.media['name']
        self.name.set(name)
        h,m,s = helper.convertSecNoToHMS(self.duration, toObj=True).values()
        self.hh.set(h)
        self.mm.set(m)
        self.ss.set(s)
        

    def initGUI(self):
        # first destroy
        if None is not self.popup:
            self.popup.destroy()
        self.popup = tk_helper.makePiepMePopup('Add to Schedule', w=400, h=250, padx=0, pady=0)
        # var
        self.name = tk.StringVar()
        self.hh = tk.StringVar()
        self.hh.trace("w", self.limitHH)
        self.mm = tk.StringVar()
        self.mm.trace("w", self.limitMM)
        self.ss = tk.StringVar()
        self.ss.trace("w", self.limitSS)
        self.setupData()
        #
        wrapper = tk.Frame(self.popup)
        wrapper.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #1. Name
        fName = tk.Frame(wrapper, pady=10, padx=20)
        lName = tk.Label(fName, text="Name:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lName.pack(side=tk.LEFT, fill=tk.Y)
        name = tk.Entry(fName, textvariable=self.name, width=100, borderwidth=5, relief=tk.FLAT)
        name.bind("<FocusIn>", lambda args: name.select_range('0', tk.END))
        name.pack(side=tk.LEFT, fill=tk.X)
        fName.pack(side=tk.TOP, fill=tk.X)
        #2. Duration
        fDura = tk.Frame(wrapper, pady=10, padx=20)
        fDura.pack(side=tk.TOP, fill=tk.X)
        #
        lDura = tk.Label(fDura, text="Duration:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lDura.pack(side=tk.LEFT, fill=tk.Y)
        ##
        self.eHH = tk.Entry(fDura, textvariable=self.hh, width=4, borderwidth=5, relief=tk.FLAT, justify=tk.CENTER)
        self.eHH.bind("<FocusIn>", lambda args: self.eHH.select_range('0', tk.END))
        self.eHH.pack(side=tk.LEFT, fill=tk.X)
        ##
        separator = tk.Label(fDura, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=5)
        ##
        self.eMM = tk.Entry(fDura, textvariable=self.mm, width=4, borderwidth=5, relief=tk.FLAT, justify=tk.CENTER)
        self.eMM.bind("<FocusIn>", lambda args: self.eMM.select_range('0', tk.END))
        self.eMM.pack(side=tk.LEFT, fill=tk.X)
        ##
        separator = tk.Label(fDura, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT)
        separator.pack(side=tk.LEFT, padx=5)
        ##
        lName.pack(side=tk.LEFT, fill=tk.Y)
        self.eSS = tk.Entry(fDura, textvariable=self.ss, width=4, borderwidth=5, relief=tk.FLAT, justify=tk.CENTER)
        self.eSS.bind("<FocusIn>", lambda args: self.eSS.select_range('0', tk.END))
        self.eSS.pack(side=tk.LEFT, fill=tk.X)
        #3. Button
        fBtn = tk.Frame(wrapper, pady=10, padx=20)
        btnCancel = tk.Button(fBtn, text="Cancel", bd=2, relief=tk.RAISED, command=self.popup.destroy)
        btnCancel.configure(width=7)
        btnCancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btnOk = tk.Button(fBtn, text="OK", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.onSave)
        btnOk.configure(width=7)
        btnOk.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        fBtn.pack(side=tk.BOTTOM, fill=tk.X)

    def limitHH(self, *arg):
       self.verifyHMS(self.hh)

    def limitMM(self, *arg):
       self.verifyHMS(self.mm)

    def limitSS(self, *arg):
       self.verifyHMS(self.ss)

    def verifyHMS(self, strvar):
        tk_helper.character_limit(strvar, limit=2)
        strvar.set(re.sub(r"^[^0-9]{2}$", '', strvar.get()))
        

    def onSave(self):
        self.parent.addToSchedule({
            'id':self.id,
            'name': self.name.get(), 
            'url': self.url, 
            'type': self.mtype,
            'duration': helper.convertHMSNoToSec({'h': self.hh.get(), 'm': self.mm.get(), 's': self.ss.get()})
        })
