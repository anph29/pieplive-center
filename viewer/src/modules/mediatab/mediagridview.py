import tkinter as tk
from src.modules.custom import DynamicGrid
from src.modules.mediabox import MediaBox
from . import MediaTab
from src.enums import MediaType
from src.modules.addresource import AddResource
from PIL import Image, ImageTk
from src.utils import helper

class MediaGridView(DynamicGrid, MediaTab):
    def __init__(self, parent, tabType=None, *args, **kwargs):
        super(MediaGridView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.tabType = tabType
        self.initUI()

    def initUI(self):
        super(MediaGridView, self).initUI()
        if self.tabType == MediaType.IMAGE or self.tabType == MediaType.VIDEO:
            self.showAddCamBtn()

    def addMediaToList(self, media):
        self.after_effect(MediaBox(self.context, parentTab=self, media=media, bg="#f2f2f2", relief=tk.FLAT, bd=3))

    def showAddCamBtn(self):
        addresource = AddResource(self)
        imAdd = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}add-rgb24-bgw.png"))
        self.cmdAdd = tk.Label(self.toolbar, image=imAdd, cursor='hand2')
        self.cmdAdd.image = imAdd
        self.cmdAdd.bind("<Button-1>", addresource.initGUI)
        self.cmdAdd.pack(side=tk.RIGHT, padx=15, pady=5)
