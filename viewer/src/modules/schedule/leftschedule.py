import tkinter as tk
from src.modules.mediatab import MediaScheduleView
from src.enums import MediaType

class LeftSchedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(LeftSchedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initUI()

    def initUI(self):
      self.schedule = MediaScheduleView(self, tabType=MediaType.SCHEDULE, bg="#ccc")
      self.schedule.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

