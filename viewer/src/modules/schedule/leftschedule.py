import tkinter as tk
from src.modules.schedulecontent import SortedList
from src.modules.schedulecontent import SingleSchedule


class ScheduleHead(tk.Frame):
    def __init__(self, parent, schedule=None, *args, **kwargs):
        super(ScheduleHead, self).__init__(parent, *args, **kwargs)
        self.sortedlist = None
        self.schedule = schedule
        self.initUI()

    def initUI(self):
        self.sortedlist = SortedList(self, bg="#fff")
        self.sortedlist.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class ScheduleDetail(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(ScheduleDetail, self).__init__(parent, *args, **kwargs)
        self.singleschedule = None
        self.initUI()

    def initUI(self):
        self.singleschedule = SingleSchedule(self, bg="#fff")
        self.singleschedule.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class LeftSchedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(LeftSchedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.mutiLeft = None
        self.mutiRight = None
        self.initUI()

    def initUI(self):
        self.mutiRight = ScheduleDetail(self, bg="#f0f0f0")
        self.mutiRight.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        #
        self.mutiLeft = ScheduleHead(
            self, schedule=self.mutiRight.singleschedule, bg="#fff"
        )
        self.mutiLeft.pack(side=tk.LEFT, fill=tk.Y)
