import tkinter as tk
from .sortedlist import SortedList
from .singleschedule import SingleSchedule


class MultiScheduleLeft(tk.Frame):
    def __init__(self, parent, schedule=None, *args, **kwargs):
        super(MultiScheduleLeft, self).__init__(parent, *args, **kwargs)
        self.sortedlist = None
        self.schedule = schedule
        self.initUI()

    def initUI(self):
        self.sortedlist = SortedList(self, bg="#fff")
        self.sortedlist.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class MultiScheduleRight(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MultiScheduleRight, self).__init__(parent, *args, **kwargs)
        self.singleschedule = None
        self.initUI()

    def initUI(self):
        self.singleschedule = SingleSchedule(self, bg="#fff")
        self.singleschedule.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class MultiSchedule(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super(MultiSchedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.mutiLeft = None
        self.mutiRight = None
        self.initUI()

    def initUI(self):
        self.mutiRight = MultiScheduleRight(self, bg='#f0f0f0')
        self.mutiRight.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        #
        self.mutiLeft = MultiScheduleLeft(self, schedule=self.mutiRight.singleschedule, bg='#fff')
        self.mutiLeft.pack(side=tk.LEFT, fill=tk.Y)
