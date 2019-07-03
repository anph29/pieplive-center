import tkinter as tk
from src.modules.login import Login
from src.utils import store

class MainMenu(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        super(MainMenu, self).__init__(parent, *args, **kwargs)

        self.login = Login(parent)
        # F
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="New", command=lambda: False)
        self.filemenu.add_command(label="Close", command=lambda: False)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=parent.quit)
        self.add_cascade(label="File", menu=self.filemenu)
        # E
        self.editmenu = tk.Menu(self, tearoff=0)
        self.editmenu.add_command(label="Delete", command=lambda: False)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Select..", command=lambda: False)
        self.editmenu.add_command(label="Select All", command=lambda: False)
        self.add_cascade(label="Edit", menu=self.editmenu)
        # H
        self.initHelpMenu()

    def initHelpMenu(self):
        self.helpmenu = tk.Menu(self, tearoff=0)
        # if login
        if bool(store._get('FO100')):
            self.helpmenu.add_command(label="Logout", command=self.login.logout)
        else:
            self.helpmenu.add_command(label="Login", command=self.login.open)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Help Index", command=lambda: False)
        self.helpmenu.add_command(label="About..", command=lambda: False)
        self.add_cascade(label="Help", menu=self.helpmenu)