from src.modules.custom import DynamicGrid
from src.modules.addresource import AddResource
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.utils import helper, store
from src.models import L500_model
from src.enums import MediaType


class MediaTab(object):

    def initUI(self):
        self.showLsMedia()

    def showLsMedia(self):
        for media in self.loadLsMedia():
            self.addMediaToList(media)

    def showAddCamBtn(self):
        addresource = AddResource(self)
        btnAddResource = tk.Frame(self, relief=tk.FLAT)
        imageAdd = ImageTk.PhotoImage(Image.open(helper._ICONS_PATH + "add-b.png"))
        lblAdd = tk.Label(btnAddResource, image=imageAdd, cursor='hand2', bg="#f2f2f2")
        lblAdd.image = imageAdd
        lblAdd.bind("<Button-1>", addresource.initGUI)
        lblAdd.pack(fill=tk.BOTH, expand=True)
        btnAddResource.place(rely=1.0, relx=1.0, x=-20, y=-20, anchor=tk.SE)

    def clearData(self, clearView=False):
        self.writeLsMedia([])
        #
        if clearView:
            self.context.config(state=tk.NORMAL)
            self.context.delete(1.0, tk.END)
            self.context.config(state=tk.DISABLED)

    def renewData(self, lsMedia):
        self.clearData(clearView=True)
        lsMedia = list(map(lambda l500: {
                    "id":  str(l500['_id']) or '',
                    "name": l500['LV501'] or '',
                    "url": l500['LV506'] or '',
                    "type": helper.getMTypeFromUrl(l500['LV506'] or '')
                }, lsMedia))
        self.writeLsMedia(lsMedia)
        self.showLsMedia()

    def addMedia(self, data):
        if self.tabType == MediaType.CAMERA:
            helper._add_to_lscam(data)
        elif self.tabType == MediaType.IMAGE:
            helper._add_to_image(data)
        elif self.tabType == MediaType.VIDEO:
            helper._add_to_video(data)
        elif self.tabType == MediaType.PRESENTER:
            helper._add_to_spresenter(data)

    def loadLsMedia(self):
        if self.tabType == MediaType.CAMERA:
            return helper._load_lscam()
        elif self.tabType == MediaType.IMAGE:
            return helper._load_image()
        elif self.tabType == MediaType.VIDEO:
            return helper._load_video()
        elif self.tabType == MediaType.PRESENTER:
            return helper._load_ls_presenter()

    def writeLsMedia(self, data):
        if self.tabType == MediaType.CAMERA:
            helper._write_lscam(data)
        elif self.tabType == MediaType.IMAGE:
            helper._write_image(data)
        elif self.tabType == MediaType.VIDEO:
            helper._write_video(data)
        elif self.tabType == MediaType.PRESENTER:
           helper._write_lspresenter(data)

    def deleteMediaItem(self, lsId):
        ls = self.loadLsMedia()
        filtered = list(filter(lambda x:x['id'] not in lsId, ls))
        # clear
        self.clearData()
        # new
        self.writeLsMedia(filtered)
