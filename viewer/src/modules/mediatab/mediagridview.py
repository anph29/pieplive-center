import tkinter as tk
from src.modules.custom import DynamicGrid
from src.modules.mediaitem import MediaItemBox
from . import MediaTab
from src.enums import MediaType
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
        self.after_effect(MediaItemBox(self.context, parentTab=self, media=media, bg="#f2f2f2", relief=tk.FLAT, bd=3))

