import tkinter as tk
from .keymanager import KeyManager
from .listp300 import ListP300


class COMLeft(tk.Frame):
    def __init__(self, parent, keyManager=None, *args, **kwargs):
        super(COMLeft, self).__init__(parent, *args, **kwargs)
        self.keyManager = keyManager
        self.initUI()

    def initUI(self):
        self.listP300 = ListP300(self, keyManager=self.keyManager, bg="#fff")
        self.listP300.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class COMRight(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(COMRight, self).__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.keyManager = KeyManager(self, bg="#fff")
        self.keyManager.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class COMWrapper(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(COMWrapper, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.left = None
        self.right = None
        self.initUI()

    def initUI(self):
        #
        self.right = COMRight(self, bg="#f0f0f0")
        self.right.pack(side=tk.RIGHT, fill=tk.Y)
        #
        self.left = COMLeft(self, keyManager=self.right.keyManager, bg="#fff")
        self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
