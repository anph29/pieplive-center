import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import random


class DynamicGrid(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(DynamicGrid, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.lsBox = []
        self.context = ScrolledText(self, wrap="char", bd=0, relief=tk.FLAT, highlightthickness=0)
        self.context.tag_configure('center', justify=tk.CENTER)
        self.context.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def getContext(self):
        return self.context

    def after_effect(self, box):
        self.lsBox.append(box)
        self.context.configure(state=tk.NORMAL)
        self.context.window_create(tk.END, window=box)
        self.context.configure(state=tk.DISABLED)
