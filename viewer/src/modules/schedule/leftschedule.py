import tkinter as tk
from src.modules.custom import DDList
class LeftSchedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(LeftSchedule, self).__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.listBox = DDList(self, 
            600,
            50,
            offset_x=5,
            offset_y=5,
            gap=5,
            item_borderwidth=1,
            item_relief=tk.FLAT,
            borderwidth=0,
            bg="#ccc")
        self.listBox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)