import tkinter as tk
from src.modules.login import Login


class MainMenu():
    def __init__(self, root):
        login = Login(self)
        menubar = tk.Menu(root)
        # F
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=lambda: False)
        filemenu.add_command(label="Open", command=lambda: False)
        filemenu.add_command(label="Save", command=lambda: False)
        filemenu.add_command(label="Save as...", command=lambda: False)
        filemenu.add_command(label="Close", command=lambda: False)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        # E
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=lambda: False)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=lambda: False)
        editmenu.add_command(label="Copy", command=lambda: False)
        editmenu.add_command(label="Paste", command=lambda: False)
        editmenu.add_command(label="Delete", command=lambda: False)
        editmenu.add_command(label="Select All", command=lambda: False)
        menubar.add_cascade(label="Edit", menu=editmenu)
        # H
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Login", command=login.open)
        editmenu.add_separator()
        helpmenu.add_command(label="Help Index", command=lambda: False)
        helpmenu.add_command(label="About..", command=lambda: False)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)
