import tkinter as tk
from src.modules.custom import PLabel
from PIL import Image, ImageTk
from src.utils import helper
from src.constants import UI
from .mediaitem import MediaItem

class MediaItemSchedule(MediaItem):
     
    def __init__(self, parent, media=None, parentTab=None, *args, **kwargs):
        super(MediaItemSchedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parentTab = parentTab
        self.set_data(media)
        self.initGUI()

    def get_data(self):
        data = super(MediaItemSchedule, self).get_data()
        data['duration'] = self.duration
        return data

    def set_data(self, media):
        super(MediaItemSchedule, self).set_data(media)
        self.duration = media['duration']

    def initGUI(self):
        #
        wrapper = tk.Frame(self, bd=10, relief=tk.FLAT, height=30)
        wrapper.pack(side=tk.BOTTOM, fill=tk.X)
        self.checkbox = tk.Checkbutton(wrapper, variable=self.checked, onvalue=True, offvalue=False, height=1, width=1, bd=0, relief=tk.FLAT)
        self.checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        lbl_name = PLabel(wrapper, text=self.name, justify=tk.LEFT, elipsis=40, font=UI.TXT_FONT, fg="#000")
        lbl_name.pack(side=tk.LEFT)
        # bin
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b.png"))
        lbl_trash = tk.Label(wrapper, image=imageBin, cursor='hand2')
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deletemedia)
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # edit
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}pen-b.png"))
        lbl_trash = tk.Label(wrapper, image=imageBin, cursor='hand2')
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.editMedia)
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #duration
        hms = helper.convertSecNoToHMS(self.duration)
        dura = PLabel(wrapper, text=hms, fg='#ff2d55', font=UI.TXT_FONT)
        dura.pack(side=tk.RIGHT, padx=10)
    
    def editMedia(self, evt):
        self.parentTab.showAddToSchedulePopup(self.get_data(), edit=True)

    def deletemedia(self, evt):
        super(MediaItemSchedule, self).deletemedia(evt)
        self.parentTab.tabRefresh(None)