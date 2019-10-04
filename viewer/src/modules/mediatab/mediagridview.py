import tkinter as tk
from src.modules.custom import DynamicGrid
from src.modules.mediaitem import MediaItemBox
from .mediatab import MediaTab
from src.enums import MediaType


class MediaGridView(DynamicGrid, MediaTab):
    def __init__(self, parent, tabType=None, *args, **kwargs):
        self.tabType = tabType
        super(MediaGridView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.ddlist = None
        self.initUI()

    def initUI(self):
        super(MediaGridView, self).initUI()
        if self.tabType not in (
            MediaType.CAMERA,
            MediaType.PRESENTER,
            MediaType.SCHEDULE,
        ):
            self.showAddCamBtn()
        # search zone
        # self.zSearch.searchZone.pack(side=tk.TOP, fill=tk.X)

    def addMediaToList(self, media):
        ui = MediaItemBox(
            self.context, parentTab=self, media=media, bg="#fff", relief=tk.FLAT, bd=3
        )
        self._LS_MEDIA_UI.append(ui)
        self.after_effect(ui)

    def clearView(self):
        super(MediaGridView, self).clearView()
        self.context.config(state=tk.NORMAL)
        self.context.delete(1.0, tk.END)
        self.context.config(state=tk.DISABLED)
