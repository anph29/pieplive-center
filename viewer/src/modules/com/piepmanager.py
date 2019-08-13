import tkinter as tk
from src.modules.custom import DynamicGrid


class PiepManager(DynamicGrid, tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(PiepManager, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self._LS_MEDIA_DATA = []
        self._LS_MEDIA_UI = []
        self.initUI()

    def initUI(self):
        pass

    def clearData(self, clearView=False):
        # self._LS_MEDIA_DATA = []
        self.writeLsMedia([])
        if clearView:
            self.clearView()
            
    def clearView(self):
        self._LS_MEDIA_UI = []
        self.context.config(state=tk.NORMAL)
        self.context.delete(1.0, tk.END)
        self.context.config(state=tk.DISABLED)
