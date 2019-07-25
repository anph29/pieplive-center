import tkinter as tk

class MultiScheduleRight(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MultiScheduleRight, self).__init__()
        self.initUI()

    def initUI(self):
        self.schedule = MediaScheduleView(self, tabType=MediaType.SCHEDULE, bg="#fff")
        self.schedule.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
