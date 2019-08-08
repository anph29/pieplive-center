import tkinter as tk
from tkinter import ttk
from src.enums import MediaType
from src.modules.mediatab import MediaListView
from src.utils import helper
class RightSchedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.schedule = kwargs['schedule']
        del kwargs['schedule']
        super(RightSchedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.scheduleTab = ttk.Notebook(self, style="sub.TNotebook")
        self.scheduleTab.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # 1
        icImg = tk.PhotoImage(file=helper._ICONS_PATH + 'ic_image.png')
        self.tab_image = self.makeMediaTab(MediaType.IMAGE)
        self.tab_image.image = icImg
        self.scheduleTab.add(self.tab_image, text="Images", image=icImg, compound=tk.LEFT)
        # 2
        icVid = tk.PhotoImage(file=helper._ICONS_PATH + 'ic_video.png')
        self.tab_video = self.makeMediaTab(MediaType.VIDEO)
        self.tab_video.image = icVid
        self.scheduleTab.add(self.tab_video, text="Videos", image=icVid, compound=tk.LEFT)
        # 3
        icCam = tk.PhotoImage(file=helper._ICONS_PATH + 'ic_camera.png')
        self.tab_camera = self.makeMediaTab(MediaType.CAMERA)
        self.tab_camera.image = icCam
        self.scheduleTab.add(self.tab_camera, text="Cameras", image=icCam, compound=tk.LEFT)
        # 4
        icPres = tk.PhotoImage(file=helper._ICONS_PATH + 'ic_presenter.png')
        self.tab_presenter = self.makeMediaTab(MediaType.PRESENTER)
        self.tab_presenter.image = icPres
        self.scheduleTab.add(self.tab_presenter, text="Presenters", image=icPres, compound=tk.LEFT)
        #
        self.scheduleTab.select(self.tab_image)
        self.scheduleTab.enable_traversal()

    def makeMediaTab(self, tType):
        return MediaListView(self, tabType=tType, schedule=self.schedule, bg="#fff")