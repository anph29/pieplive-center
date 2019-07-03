import tkinter as tk
from tkinter import ttk
from src.utils import helper
from src.modules.mediatab import MediaTab, TabType


class MainView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MainView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.after(100, self.initGUI)

    def set_style(self):
        style = ttk.Style()
        style.theme_create("TabStyle", parent="alt", settings={
            "TNotebook": {
                "configure": {"tabmargins": [10, 0, 0, 10]}  # L T B R
            },
            "TNotebook.Tab": {
                "configure": {"padding": [15, 5, 15, 5]}
            }
        })
        style.theme_use("TabStyle")

    def initGUI(self):
        self.set_style()
        #
        nb = ttk.Notebook(self)
        nb.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #
        self.tab_custom = self.initTabContent(TabType.CUSTOM)
        nb.add(self.tab_custom, text="Custom Resource")
        #
        self.tab_camera = self.initTabContent(TabType.CAMERA)
        nb.add(self.tab_camera, text="Camera")
        #
        self.tab_presenter = self.initTabContent(TabType.PRESENTER)
        nb.add(self.tab_presenter, text="Presenter")
        #
        nb.select(self.tab_camera)
        nb.enable_traversal()

    def initTabContent(self, tType):
        return MediaTab(self, tabType=tType, borderwidth=0, bg="#ccc")