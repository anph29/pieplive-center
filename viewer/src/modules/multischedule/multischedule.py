import tkinter as tk
from .multischeduleleft import MultiScheduleLeft
from .multischeduleright import MultiScheduleRight


class MultiSchedule(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super(MultiSchedule, self).__init__()
        self.parent = parent
        self.mutiLeft = None
        self.mutiRight = None
        self.initUI()

    def initUI(self):
        #
        self.mutiLeft = MultiScheduleLeft(self, bg='#f00', width=240)
        self.mutiLeft.pack(side=tk.LEFT, fill=tk.BOTH)
        #
        self.mutiRight = MultiScheduleRight(self, bg='#00f')
        self.mutiRight.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)