import tkinter as tk
from src.modules.custom import DDList
from . import MediaTab
from src.modules.mediabox import MediaItemLs

class MediaListView(DDList, MediaTab):
    def __init__(self, parent, *args, **kwargs):
        self.tabType = kwargs['tabType']
        del kwargs['tabType']
        super(MediaListView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initUI()

    def addMediaToList(self, media):
        item = self.create_item()
        medi = MediaItemLs(item, parentTab=self, media=media)
        medi.pack(anchor=tk.W, padx= (4,0), pady= (4,0))
        self.add_item(item)

    def deleteMediaItem(self, lsId):
        super(MediaItemLs, self).deleteMediaItem(lsId)
        # self.delete_item()