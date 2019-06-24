import tkinter as tk


class BottomLeft(tk.PanedWindow):
    def __init__(self, parent, *args, **kwargs):
        super(BottomLeft, self).__init__(parent, *args, **kwargs)
        self.parent = parent
