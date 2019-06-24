import tkinter as tk


class ControlView(tk.PanedWindow):
    def __init__(self, parent, *args, **kwargs):
        super(ControlView, self).__init__(parent, *args, **kwargs)
        self.parent = parent