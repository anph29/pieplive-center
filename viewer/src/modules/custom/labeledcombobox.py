import tkinter as tk
from tkinter import ttk


class LabeledCombobox(tk.Frame):
    def __init__(self, master, dictionary, callback=None, selected=None, *args, **kw):
        tk.Frame.__init__(self, master, *args, **kw)
        self.dictionary = dictionary
        self.onSelectCallback = callback
        self.combo = ttk.Combobox(
            self, values=list(dictionary.keys()), width=30, state="readonly"
        )
        self.combo.config(font=("Arial", 10))
        self.combo.pack(fill=tk.BOTH)
        self.selected = selected
        self.combo.bind("<<ComboboxSelected>>", self.onSelection)

        if bool(self.dictionary):
            allValue = list(self.dictionary.values())
            idx = 0 if not bool(selected) else allValue.index(self.selected)
            self.combo.current(idx)
            self.onSelection(self.dictionary[list(dictionary.keys())[idx]])

    def onSelection(self, event):
        self.onSelectCallback(self.dictionary[self.combo.get()])

