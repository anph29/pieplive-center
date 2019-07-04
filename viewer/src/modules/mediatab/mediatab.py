from src.modules.custom import DynamicGrid
from src.modules.addresource import AddResource
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.utils import helper, store
from src.modules.mediabox import MediaBox
from src.models import L500_model
from src.enums import TabType


class MediaTab(DynamicGrid):
    
    def __init__(self, parent, tabType=TabType.CAMERA, *args, **kwargs):
        super(MediaTab, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.tabType = tabType
        self.initUI()

    def initUI(self):
        if self.tabType == TabType.IMAGE or self.tabType == TabType.VIDEO:
            self.showAddCamBtn()

        for media in self.loadLsMedia():
            self.addMediaBoxToList(media)

    def addMediaBoxToList(self, media):
        ctxt = self.getContext()
        box = MediaBox(ctxt, media=media, bg="#f2f2f2", relief=tk.FLAT, bd=3)
        self.after_effect(box)

    def showAddCamBtn(self):
        addresource = AddResource(self)
        btnAddResource = tk.Frame(self, relief=tk.FLAT)
        imageAdd = ImageTk.PhotoImage(Image.open(helper._ICONS_PATH + "add-b.png"))
        lblAdd = tk.Label(btnAddResource, image=imageAdd, cursor='hand2', bg="#f2f2f2")
        lblAdd.image = imageAdd
        lblAdd.bind("<Button-1>", addresource.initGUI)
        lblAdd.pack(fill=tk.BOTH, expand=True)
        btnAddResource.place(rely=1.0, relx=1.0, x=-20, y=-20, anchor=tk.SE)

    def addMedia(self, Fdata):
        if self.tabType == TabType.CAMERA:
            helper._add_to_lscam(data)
        elif self.tabType == TabType.IMAGE:
            helper._add_to_image(data)
        elif self.tabType == TabType.VIDEO:
            helper._add_to_video(data)
        elif self.tabType == TabType.PRESENTER:
            helper._add_to_spresenter(data)

    def loadLsMedia(self):
        if self.tabType == TabType.CAMERA:
            return helper._load_lscam()
        elif self.tabType == TabType.IMAGE:
            return helper._load_image()
        elif self.tabType == TabType.VIDEO:
            return helper._load_video()
        elif self.tabType == TabType.PRESENTER:
            return helper._load_ls_presenter()

    def writeLsMedia(self, data):
        if self.tabType == TabType.CAMERA:
            helper._write_lscam(data)
        elif self.tabType == TabType.IMAGE:
            helper._write_image(data)
        elif self.tabType == TabType.VIDEO:
            helper._write_video(data)
        elif self.tabType == TabType.PRESENTER:
           helper._write_lspresenter(data)

    def delMediaBox(self):
        pass

    