from src.modules.custom import DynamicGrid
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.utils import helper, store
from src.models import L500_model
from src.enums import MediaType
from src.modules.addresource import AddResource
from src.modules.custom import ToolTip
class MediaTab(tk.Frame):

    def __init__(self,  parent, *args, **kwargs):
        super(MediaTab, self).__init__( parent, *args, **kwargs)

    def initUI(self):
        self.showToolBar()
        self.showLsMedia()

    def showToolBar(self):
        self.checkall = tk.BooleanVar()
        self.toolbar = tk.Frame(self, height=50, relief=tk.FLAT, bg="#fff")
        self.toolbar.pack(fil=tk.X, side=tk.BOTTOM)
        # select all
        self.checkbox = tk.Checkbutton(self.toolbar , variable=self.checkall, onvalue=True, offvalue=False, height=3, width=3,bg='#fff', bd=0, cursor='hand2')
        self.checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=0)
        ToolTip(self.checkbox, 'Select all media')
        # delete all
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b24-bgw.png"))
        self.cmdDelAll = tk.Label(self.toolbar, image=imageBin, cursor='hand2', bg='#fff')
        self.cmdDelAll.image = imageBin
        self.cmdDelAll.bind("<Button-1>", lambda x:x)
        self.cmdDelAll.pack(side=tk.RIGHT, padx=(0, 15), pady=5)
        ToolTip(self.cmdDelAll, "Delete all selected")
        # refresh
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}f5-b24.png"))
        self.cmdF5 = tk.Label(self.toolbar, image=imageBin, cursor='hand2', bg='#fff')
        self.cmdF5.image = imageBin
        self.cmdF5.bind("<Button-1>", lambda x:x)
        self.cmdF5.pack(side=tk.RIGHT, padx=(0, 15), pady=5)
        ToolTip(self.cmdF5, "Refresh")
        
    def showAddCamBtn(self):
        addresource = AddResource(self)
        imAdd = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}add-rgb24-bgw.png"))
        self.cmdAdd = tk.Label(self.toolbar, image=imAdd, cursor='hand2')
        self.cmdAdd.image = imAdd
        self.cmdAdd.bind("<Button-1>", addresource.initGUI)
        self.cmdAdd.pack(side=tk.RIGHT, padx=15, pady=5)
        ToolTip(self.cmdAdd, "Add new media")

    def showLsMedia(self):
        for media in self.loadLsMedia():
            self.addMediaToList(media)

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
