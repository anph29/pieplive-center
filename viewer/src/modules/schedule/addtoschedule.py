import tkinter as tk
from src.utils import  tk_helper
from src.constants import UI

class AddToSchedule(object):
    addToSchedulePop = None

    def __init__(self, parent):
        self.parent = parent

    def initGUI(self, evt):
        # first destroy
        if None is not self.addToSchedulePop:
            self.addToSchedulePop.destroy()

        self.addToSchedulePop = tk_helper.makePiepMePopup('Add to Schedule', w=400, h=250, padx=0, pady=0)
        #
        wrapper = tk.Frame(self.addToSchedulePop)
        # var
        self.name = tk.StringVar()
        self.hh = tk.StringVar()
        self.mm = tk.StringVar()
        self.ss = tk.StringVar()
       
        # name
        fName = tk.Frame(wrapper, pady=10, padx=20)
        lName = tk.Label(fName, text="Name:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lName.pack(side=tk.LEFT, fill=tk.Y)
        eName = tk.Entry(fName, textvariable=self.name, width=100, borderwidth=5, relief=tk.FLAT)
        eName.pack(side=tk.LEFT, fill=tk.X)
        fName.pack(side=tk.TOP, fill=tk.X)
        
        # Duration
        fDura = tk.Frame(wrapper, pady=10, padx=20)
        fDura.pack(side=tk.TOP, fill=tk.X)
        #
        lDura = tk.Label(fDura, text="Duration:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lDura.pack(side=tk.LEFT, fill=tk.Y)
        ##
        eHH = tk.Entry(fDura, textvariable=self.hh, width=2, borderwidth=5, relief=tk.FLAT)
        eHH.pack(side=tk.LEFT, fill=tk.X)
        ##
        tk.Label(fName, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT).pack(side=tk.LEFT)
        ##
        eMM = tk.Entry(fDura, textvariable=self.mm, width=2, borderwidth=5, relief=tk.FLAT)
        eMM.pack(side=tk.LEFT, fill=tk.X)
        ##
        tk.Label(fName, text=":", width=1, anchor=tk.W, font=UI.TXT_FONT).pack(side=tk.LEFT)
        ##
        lName.pack(side=tk.LEFT, fill=tk.Y)
        eSS = tk.Entry(fDura, textvariable=self.ss, width=2, borderwidth=5, relief=tk.FLAT)
        eSS.pack(side=tk.LEFT, fill=tk.X)
       
        # bot button
        fBtn = tk.Frame(wrapper, pady=10, padx=20)
        btnCancel = tk.Button(fBtn, text="Cancel", bd=2, relief=tk.RAISED, command=self.addToSchedulePop.destroy)
        btnCancel.configure(width=7)
        btnCancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btnOk = tk.Button(fBtn, text="OK", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.onSave)
        btnOk.configure(width=7)
        btnOk.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        fBtn.pack(side=tk.BOTTOM, fill=tk.X)

    def onSave(self):
        pass
