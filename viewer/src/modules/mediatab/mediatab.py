from src.modules.custom import DynamicGrid
from src.modules.addresource import AddResource
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.utils import helper, store
from src.models import L500_model
from src.enums import TabType


class MediaTab(object):

    def initUI(self):
        if self.tabType == TabType.IMAGE or self.tabType == TabType.VIDEO:
            self.showAddCamBtn()
        self.showLsMedia()

    def showLsMedia(self):
        for media in self.loadLsMedia():
            self.addMediaBoxToList(media)

    def showAddCamBtn(self):
        addresource = AddResource(self)
        btnAddResource = tk.Frame(self, relief=tk.FLAT)
        imageAdd = ImageTk.PhotoImage(Image.open(helper._ICONS_PATH + "add-b.png"))
        lblAdd = tk.Label(btnAddResource, image=imageAdd, cursor='hand2', bg="#f2f2f2")
        lblAdd.image = imageAdd
        lblAdd.bind("<Button-1>", addresource.initGUI)
        lblAdd.pack(fill=tk.BOTH, expand=True)
        btnAddResource.place(rely=1.0, relx=1.0, x=-20, y=-20, anchor=tk.SE)

    def clearData(self):
        self.writeLsMedia([])
        self.context.config(state=tk.NORMAL)
        self.context.delete(1.0, tk.END)
        self.context.config(state=tk.DISABLED)

    def renewData(self, lsMedia):
        self.clearData()
        lsMedia = list(map(lambda l500: {
                    "id":  str(l500['_id']) or '',
                    "name": l500['LV501'] or '',
                    "url": l500['LV506'] or '',
                    "type": helper.getMTypeFromUrl(l500['LV506'] or '')
                }, lsMedia))
        self.writeLsMedia(lsMedia)
        self.showLsMedia()

    def addMedia(self, data):
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

    def delMediaBox(self, lsId):
        ls = self.loadLsMedia()
        filtered = list(filter(lambda x:x['id'] not in lsId, ls))
        # clear
        self.clearData()
        # new
        self.writeLsMedia(filtered)
        self.showLsMedia()
