import tkinter as tk
from src.modules.custom import DynamicGrid
from src.modules.mediabox import MediaBox
from . import MediaTab
from src.enums import MediaType

class MediaGridView(DynamicGrid, MediaTab):
    def __init__(self, parent, tabType=None, *args, **kwargs):
        super(MediaGridView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.tabType = tabType
        self.initUI()

    def initUI(self):
        if self.tabType == MediaType.IMAGE or self.tabType == MediaType.VIDEO:
            self.showAddCamBtn()
        super(MediaGridView, self).initUI()

    def addMediaToList(self, media):
        self.after_effect(MediaBox(self.context, parentTab=self, media=media, bg="#f2f2f2", relief=tk.FLAT, bd=3))
