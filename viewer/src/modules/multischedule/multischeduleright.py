import tkinter as tk
from .singleschedule import SingleSchedule


class MultiScheduleRight(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MultiScheduleRight, self).__init__(parent, *args, **kwargs)
        self.schedule = None

    def initUI(self):
        self.schedule = SingleSchedule(self, bg="#fff")
        self.schedule.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

   