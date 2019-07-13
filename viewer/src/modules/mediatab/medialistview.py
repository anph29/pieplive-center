import tkinter as tk
from src.modules.custom import DDList
from . import MediaTab
from src.modules.mediabox import MediaItemDnD
from PIL import ImageTk, Image
from src.utils import helper

class MediaListView(DDList, MediaTab):
    def __init__(self, parent, *args, **kwargs):
        self.tabType = kwargs['tabType']
        del kwargs['tabType']
        super(MediaListView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initUI()

    def initUI(self):
        super(MediaListView, self).initUI()
        # save update
        self.saveSortedMediaLst()

    def addMediaToList(self, media):
        item = self.create_item()
        medi = MediaItemDnD(item, parentTab=self, media=media)
        medi.pack(padx= (4,0), pady= (4,0), expand=True)
        self.add_item(item)

    def saveSortedMediaLst(self):
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}check-green.png"))
        self.cmdDelAll = tk.Label(self.toolbar, image=imageBin, cursor='hand2', bg='#fff')
        self.cmdDelAll.image = imageBin
        self.cmdDelAll.bind("<Button-1>", lambda x:x)
        self.cmdDelAll.pack(side=tk.RIGHT, padx=(0, 15), pady=5)
