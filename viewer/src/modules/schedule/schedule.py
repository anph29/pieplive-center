import tkinter as tk
from .leftschedule import LeftSchedule
from .rightschedule import RightSchedule

class Schedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(Schedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.left = LeftSchedule(self, bg='#fff')
        self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #
        self.right = RightSchedule(self, schedule=self.left.mutiRight.singleschedule, width=410, bg='#fff')
        self.right.pack(side=tk.RIGHT, fill=tk.Y)