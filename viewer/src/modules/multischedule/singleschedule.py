import tkinter as tk
from .scheduleddlist import ScheduleDDList
from src.modules.custom import DDList


class SingleSchedule(ScheduleDDList):

    def __init__(self, parent, *args, **kwargs):
        super(SingleSchedule, self).__init__(parent, *args, **kwargs)

    def makeDDList(self, ref):
        return DDList(ref,
            400,
            42,
            offset_x=5,
            offset_y=5,
            gap=5,
            item_borderwidth=1,
            item_relief=tk.FLAT,
            borderwidth=0,
            bg="#fff",
            droppedCallback=self.saveSortedList)
    
    def initUI(self):
        super(SingleSchedule, self).initUI()
        #
        self.scrollZ.pack(fill=tk.BOTH, expand=True)
        self.ddlist.pack(fill=tk.Y, expand=True)
