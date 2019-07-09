import tkinter as tk
from src.modules.custom import DragDropListbox
from . import MediaTab

class MediaListView(DragDropListbox, MediaTab):
    def __init__(self, parent, tabType=None, *args, **kwargs):
        super(MediaGridView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.tabType = tabType
        self.initUI()


    def addMediaBoxToList(self, media):
        pass