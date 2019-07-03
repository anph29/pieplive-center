import tkinter as tk
from tkinter import ttk


class LabeledCombobox(tk.Frame):

    def __init__(self, master, dictionary, callback=None, *args, **kw):
        tk.Frame.__init__(self, master, *args, **kw)
        self.dictionary = dictionary
        self.onSelectCallback = callback
        self.combo = ttk.Combobox(self, values=sorted(list(dictionary.keys())),state='readonly')
        self.combo.current(0)
        self.combo.pack(fill="both")
        self.combo.bind('<<ComboboxSelected>>', self.onSelection)

    def onSelection(self, event=None):
        self.onSelectCallback(self.dictionary[self.combo.get()])



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Labeled comboboxes")

    lookup = {'Arkitekt': 'A', 'Geoteknik': 'B',
            'Ingeniør Anlæg': 'C', 'Procesanlæg': 'D'}

    documentcode = {'Aftaler': 'AGR', 'Analyse': 'ANA',
                    'Myndigheder': 'AUT', 'Sagsbasis': 'BAS'}

    combo1 = LabeledCombobox(root, lookup, bd=1, relief="groove")
    combo1.pack(side="left", padx=(2, 2), pady=5)
    combo2 = LabeledCombobox(root, documentcode, bd=1, relief="groove")
    combo2.pack(side="right", padx=(2, 2), pady=5)

    root.mainloop()