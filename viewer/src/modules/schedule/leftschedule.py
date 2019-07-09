import tkinter as tk
from src.modules.custom import DragDropListbox
class LeftSchedule(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(LeftSchedule, self).__init__(parent, *args, **kwargs)

    def initUI(self):
        self.listBox = DragDropListbox(self)
        self.listBox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)