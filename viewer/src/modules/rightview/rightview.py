import tkinter as tk
from tkinter import ttk
from src.utils import helper
from src.modules.custom import DynamicGrid
from .mediabox import MediaBox
from PIL import Image, ImageTk
from .addcamera import AddCamera


class RightView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(RightView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.after(100, self.initGUI)

    def set_style(self):
        style = ttk.Style()
        style.theme_create("AnphStyle", parent="alt", settings={
            "TNotebook": {
                "configure": {"tabmargins": [0, 0, 0, 0]}  # L T B R
            },
            "TNotebook.Tab": {
                "configure": {"padding": [15, 5, 15, 5]}
            }
        })
        style.theme_use("AnphStyle")

    def initGUI(self):
        self.set_style()
        # Make the notebook
        nb = ttk.Notebook(self)
        nb.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # Make 1st tab
        self.tab_camera = DynamicGrid(self, borderwidth=0, bg="#fff")
        self.mkTabCamera()
        # Add the tab
        nb.add(self.tab_camera, text="Camera")

        # Make 2nd tab
        self.tab_presenter = DynamicGrid(self, borderwidth=0, bg="#fff")
        self.mkTabPresenter()
        # Add 2nd tab
        nb.add(self.tab_presenter, text="Presenter")
        #
        nb.select(self.tab_camera)
        nb.enable_traversal()

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
        box = MediaBox(ctxt, camera=cam, bg="#fff",
                       relief=tk.FLAT, borderwidth=5, width=240, height=135)
        self.tab_camera.after_effect(box)

    def addToTabPresenter(self, cam):
        ctxt = self.tab_presenter.getContext()
        box = MediaBox(ctxt, camera=cam, bg="#fff",
                       relief=tk.FLAT, borderwidth=5, width=240, height=135)
        self.tab_presenter.after_effect(box)

    def showAddCamBtn(self):
        addcamera = AddCamera(self)
        # add camera
        btnAddCamera = tk.Frame(
            self,  relief=tk.FLAT, bg='#fff', borderwidth=5)
        imageAdd = ImageTk.PhotoImage(Image.open("src/icons/add-b.png"))
        lblAdd = tk.Label(btnAddCamera, image=imageAdd,
                          cursor='hand2', bg="#f2f2f2")
        lblAdd.image = imageAdd
        lblAdd.bind("<Button-1>", addcamera.openAddCamera)
        lblAdd.pack(fill=tk.BOTH, expand=True)
        self.tab_camera.after_effect(btnAddCamera)
