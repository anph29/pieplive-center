import tkinter as tk
from tkinter import ttk
from src.utils import helper
from src.modules.custom import DynamicGrid
from .mediabox import MediaBox
from PIL import Image, ImageTk
from .addresource import AddResource


class RightView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(RightView, self).__init__(parent, *args, **kwargs)
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
        self.tab_custom = self.makeGirdForTab()
        # self.mkTabCamera()
        nb.add(self.tab_custom, text="Custom Resource")
        #
        self.tab_schedule = self.makeGirdForTab()
        # self.mkTabPresenter()
        nb.add(self.tab_schedule, text="Schedule")
        #
        self.tab_camera = self.makeGirdForTab()
        self.mkTabCamera()
        nb.add(self.tab_camera, text="Camera")
        #
        self.tab_presenter = self.makeGirdForTab()
        self.mkTabPresenter()
        nb.add(self.tab_presenter, text="Presenter")

        #
        nb.select(self.tab_custom)
        nb.enable_traversal()

    def makeGirdForTab(self):
        return DynamicGrid(self, borderwidth=0, bg="#ccc")

    def mkTabCamera(self):
        self.showAddCamBtn()
        for cam in helper._load_lscam():
            self.addToTabCamera(cam)
        self.tab_camera.pack(fill=tk.BOTH, expand=True)

    def mkTabPresenter(self):
        for cam in helper._load_ls_presenter():
            self.addToTabPresenter(cam)
        self.tab_presenter.pack(fill=tk.BOTH, expand=True)

    def addToTabCamera(self, cam):
        ctxt = self.tab_camera.getContext()
        box = MediaBox(ctxt, camera=cam, bg="#ccc",
                       relief=tk.FLAT, borderwidth=5, width=240, height=135)
        self.tab_camera.after_effect(box)

    def addToTabPresenter(self, cam):
        ctxt = self.tab_presenter.getContext()
        box = MediaBox(ctxt, camera=cam, bg="#ccc",
                       relief=tk.FLAT, borderwidth=5, width=240, height=135)
        self.tab_presenter.after_effect(box)

    def showAddCamBtn(self):
        addresource = AddResource(self)
        # add camera
        btnAddResource = tk.Frame(self,  relief=tk.FLAT)
        imageAdd = ImageTk.PhotoImage(Image.open(helper._ICONS_PATH + "add-b.png"))
        lblAdd = tk.Label(btnAddResource, image=imageAdd, cursor='hand2', bg="#f2f2f2")
        lblAdd.image = imageAdd
        lblAdd.bind("<Button-1>", addresource.initGUI)
        lblAdd.pack(fill=tk.BOTH, expand=True)
        btnAddResource.place(rely=1.0, relx=1.0, x=-20, y=-20, anchor=tk.SE)
