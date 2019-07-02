import tkinter as tk
from src.modules.login import Login
from src.utils import store

class MainMenu():
    def __init__(self, root):
        self.login = Login(root)
        self.menubar = tk.Menu(root)
        # F
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=lambda: False)
        self.filemenu.add_command(label="Close", command=lambda: False)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        # E
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Delete", command=lambda: False)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Select..", command=lambda: False)
        self.editmenu.add_command(label="Select All", command=lambda: False)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        # H
        self.initHelpMenu()

        root.config(menu=self.menubar)
        
    def initHelpMenu(self):
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        # if not lign
        if store._get('FO100') == None:
            self.helpmenu.add_command(label="Login", command=self.login.open)
        else:
            self.helpmenu.add_command(label="Logout", command=self.login.logout)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Help Index", command=lambda: False)
        self.helpmenu.add_command(label="About..", command=lambda: False)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)