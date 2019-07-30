import tkinter as tk
from .multischeduleleft import MultiScheduleLeft
from .multischeduleright import MultiScheduleRight


class MultiSchedule(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super(MultiSchedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.mutiLeft = None
        self.mutiRight = None
        self.initUI()

    def initUI(self):
        #
        self.mutiLeft = MultiScheduleLeft(self, bg='#fff')
        self.mutiLeft.pack(side=tk.LEFT, fill=tk.Y)
        #
        self.mutiRight = MultiScheduleRight(self, bg='#f0f0f0')
        self.mutiRight.pack(side=tk.LEFT, fill=tk.Y)
