import tkinter as tk
from .multischeduleleft import MultiScheduleLeft
from .multischeduleright import MultiScheduleRight
class MultiSchedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MultiSchedule, self).__init__()
        self.initUI()

    def initUI(self):
        self.mutiLeft = MultiScheduleLeft(self, bg='#fff', width=240)
        self.mutiLeft.pack(side=tk.LEFT, fill=tk.Y)
        #
        self.mutiRight = MultiScheduleRight(self, bg='#fff')
        self.mutiRight.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)