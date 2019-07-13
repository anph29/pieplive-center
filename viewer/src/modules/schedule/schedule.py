import tkinter as tk
from .leftschedule import LeftSchedule
from .rightschedule import RightSchedule

class Schedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(Schedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initUI()

    def initUI(self):
        #
        self.left = LeftSchedule(self)
        self.left.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        #
        self.right = RightSchedule(self)
        self.right.grid(row=0, column=2, sticky=tk.NSEW)
        #
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_columnconfigure(2, weight=1, uniform="group1")
        self.grid_rowconfigure(0, weight=1)