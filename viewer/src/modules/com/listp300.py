import tkinter as tk
from src.modules.custom import DynamicGrid
from p300box import P300Box

class ListP300(DynamicGrid, tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(ListP300, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self._LS_P300_DATA = []
        self._LS_P300_UI = []
        self.initUI()

    def initUI(self):
        pass

    def addPiepToList(self, p300):
        ui = P300Box(self.context, p300, bg="#fff", relief=tk.FLAT, bd=3)
        self._LS_P300_UI.append(ui)
        self.after_effect(ui)

    def clearData(self, clearView=False):
        # self._LS_P300_DATA = []
        self.writeLsMedia([])
        if clearView:
            self.clearView()

    def clearView(self):
        self._LS_P300_UI = []
        self.context.config(state=tk.NORMAL)
        self.context.delete(1.0, tk.END)
        self.context.config(state=tk.DISABLED)
