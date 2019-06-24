import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import random


class DynamicGrid(tk.Frame):
    def __init__(self, parent,  *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.context = ScrolledText(self, wrap="char", borderwidth=0, highlightthickness=0,
                                    state="disabled")
        self.boxes = []
        self.context.pack(fill=tk.BOTH, expand=True)

    def getContext(self):
        return self.context

    def after_effect(self, box):
        self.boxes.append(box)
        self.context.configure(state="normal")
        self.context.window_create("end", window=box)
        self.context.configure(state="disabled")
