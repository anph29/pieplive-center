import tkinter as tk
from src.enums import TabType
from src.modules.mediatab import MediaListView
class RightSchedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(RightSchedule, self).__init__(parent, *args, **kwargs)

    def initUI(self):
        self.scheduleTab = ttk.Notebook(self)
        self.scheduleTab.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # 1
        self.tab_image = self.initTabContent(TabType.IMAGE)
        self.scheduleTab.add(self.tab_image, text="Images")
        # 2
        self.tab_video = self.initTabContent(TabType.VIDEO)
        self.scheduleTab.add(self.tab_video, text="Videos")
        # 3
        self.tab_camera = self.initTabContent(TabType.CAMERA)
        self.scheduleTab.add(self.tab_camera, text="Cameras")
        # 4
        self.tab_presenter = self.initTabContent(TabType.PRESENTER)
        self.scheduleTab.add(self.tab_presenter, text="Presenters")
        #
        self.scheduleTab.select(self.tab_image)
        self.scheduleTab.enable_traversal()

    def initTabContent(self, tType):
        return MediaListView(self, tabType=tType, borderwidth=0, bg="#ccc")