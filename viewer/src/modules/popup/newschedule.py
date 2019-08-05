import tkinter as tk
from src.utils import tk_helper

class PopupNewSchedule(object):

    def __init__(self, parent, data):
        self.parent = parent
        self.media = data
        self.popup = None

    def setupData(self):
        self.mtype = self.media['type']
        self.duration = int(self.media['duration']) if 'duration' in self.media else 0
        self.id = self.media['id']
        #
        name = self.media['name']
        url = self.media['url']
        self.name.set(name)
        self.url.set(url)

    def initGUI(self, data):
        # first destroy
        if None is not self.popup:
            self.popup.destroy()
        self.popup = tk_helper.makePiepMePopup('New Schedule', w=300, h=320, padx=0, pady=0)
        self.initUI()

    def initUI(self):
        fFile = tk.Frame(self.popup)
        # var
        self.name = tk.StringVar()
        self.url = tk.StringVar()
        self.setupData()
       
       
        # bot button
        fBtn = tk.Frame(fFile, pady=10, padx=20)
        btnCancel = tk.Button(fBtn, text="Cancel", bd=2, relief=tk.RAISED, command=self.popup.destroy)
        btnCancel.configure(width=7)
        btnCancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btnOk = tk.Button(fBtn, text="OK", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.onSave)
        btnOk.configure(width=7)
        btnOk.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        fBtn.pack(side=tk.BOTTOM, fill=tk.X)
        fFile.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def onSave(self):
        self.parent.saveToMediaList({
            'id':self.id,
            'name': self.name.get(), 
            'path': self.path, 
        })
        self.popup.destroy()