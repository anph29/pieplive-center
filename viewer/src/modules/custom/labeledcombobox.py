import tkinter as tk
from tkinter import ttk


class LabeledCombobox(tk.Frame):

    def __init__(self, master, dictionary, callback=None, *args, **kw):

        tk.Frame.__init__(self, master, *args, **kw)
        self.dictionary = dictionary
        self.onSelectCallback = callback
        self.combo = ttk.Combobox(self, values=sorted(list(dictionary.keys())), width=30, state='readonly')
        self.combo.config(font=("Arial", 10))
        if bool(self.dictionary):
            self.combo.current(0)
        self.combo.pack(fill=tk.BOTH)
        self.combo.bind('<<ComboboxSelected>>', self.onSelection)

    def onSelection(self, event=None):
        self.onSelectCallback(self.dictionary[self.combo.get()])
