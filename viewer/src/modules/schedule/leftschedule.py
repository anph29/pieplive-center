import tkinter as tk
from src.modules.custom import DDList, VerticalScrolledFrame, ToolTip
from src.modules.mediaitem import MediaItemSchedule
from src.utils import helper

class LeftSchedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(LeftSchedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.scrollZ = VerticalScrolledFrame(self)
        self.ddlist = self.makeDDList(self.scrollZ.interior)
        self.initUI()

    def initUI(self):
        self.showLsMedia()
        self.scrollZ.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ddlist.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def makeDDList(self, ref):
        return DDList(ref, 
            400,
            50,
            offset_x=5,
            offset_y=5,
            gap=5,
            item_borderwidth=1,
            item_relief=tk.FLAT,
            borderwidth=0,
            bg="#ccc")

    def addMediaToList(self, media):
        item = self.ddlist.create_item()
        medi = MediaItemSchedule(item, media=media)
        medi.pack(padx= (4,0), pady= (4,0), expand=True)
        self.ddlist.add_item(item)

    def showLsMedia(self):
        for media in helper._load_schedule():
            self.addMediaToList(media)
