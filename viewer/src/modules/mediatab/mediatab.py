import tkinter as tk
from tkinter import messagebox
import PIL
from PIL import Image, ImageTk
from src.utils import helper
from src.enums import MediaType
from src.modules.popup import PopupAddResource
from src.modules.custom import ToolTip
from src.utils import firebase, store
from src.modules.login import Login

class MediaTab(tk.Frame):

    def __init__(self,  parent, *args, **kwargs):
        super(MediaTab, self).__init__( parent, *args, **kwargs)
        self.parent = parent
        self.tbBgColor = '#fff'
        self._LS_MEDIA_DATA = []
        self._LS_MEDIA_UI = []
        self.listenerStream = None
        self.tabType = None
        self.totalDuration = 0

    def initUI(self):
        self.showLsMedia()
        self.showToolBar()
        self.after(500, self.turnOnObserver)
        firebase.makeChangePresenter(0)

    def turnOnObserver(self):
        if bool(store._get('FO100')) and self.tabType == MediaType.PRESENTER:
            firebase.startObserverActivedBu(self.firebaseCallback)

    def firebaseCallback(self, message):
        data = message['data']
        id = ln510 = 0
        if bool(data):
            if message['path'] == '/': # case init: get multi data
                keys = list(data.keys())
                for k in keys:
                    media = data[k]
                    id = int(media['_id'])
                    ln510 = int(media['LN510'])
                    self.changeStatePresenter(id, ln510)
            else:# </PL500> case change: get single data
                id = int(data['_id'])
                ln510 = int(data['LN510'])
                self.changeStatePresenter(id, ln510)

    def changeStatePresenter(self, id, ln510):
        for m in self._LS_MEDIA_UI:
            if int(m.id) == id:
                m.updateLightColor(ln510)

    def stopListenerStream(self):
        if self.tabType == MediaType.PRESENTER and bool(self.listenerStream):
            self.listenerStream.close()

    def showToolBar(self):
        self.checkall = tk.BooleanVar()
        self.toolbar = tk.Frame(self, height=50, relief=tk.FLAT, bg=self.tbBgColor)
        self.toolbar.pack(fil=tk.X, side=tk.BOTTOM)
        self.packLeftToolbar()
        self.packRightToolbar()

    def packLeftToolbar(self):
        self.tbleft = tk.Frame(self.toolbar, relief=tk.FLAT, bg=self.tbBgColor)
        self.tbleft.pack(fil=tk.Y, side=tk.LEFT)
        self.showSelectAll()
        
    def showSelectAll(self):
        # select all
        self.checkbox = tk.Checkbutton(self.tbleft , variable=self.checkall, onvalue=True, offvalue=False, height=2, width=2, bg=self.tbBgColor, bd=0, cursor='hand2', command=self.tabSelectAll)
        self.checkbox.pack(side=tk.LEFT, fill=tk.Y)
        ToolTip(self.checkbox, 'Select all media')
    
    def packRightToolbar(self):
        self.tbright = tk.Frame(self.toolbar, relief=tk.FLAT, bg=self.tbBgColor)
        self.tbright.pack(fil=tk.Y, side=tk.RIGHT)
        # delete all
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b24.png"))
        self.cmdDelAll = tk.Label(self.tbright, image=imageBin, cursor='hand2', bg=self.tbBgColor)
        self.cmdDelAll.image = imageBin
        self.cmdDelAll.bind("<Button-1>", self.tabDeleteAll)
        self.cmdDelAll.pack(side=tk.RIGHT, padx=(0, 15), pady=5)
        ToolTip(self.cmdDelAll, "Delete all selected")
        # refresh
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}f5-b24.png"))
        self.cmdF5 = tk.Label(self.tbright, image=imageBin, cursor='hand2', bg=self.tbBgColor)
        self.cmdF5.image = imageBin
        self.cmdF5.bind("<Button-1>", self.tabRefresh)
        self.cmdF5.pack(side=tk.RIGHT, padx=(0, 5), pady=5)
        ToolTip(self.cmdF5, "Refresh")

    def tabRefresh(self, evt):
        self.clearView()
        self.showLsMedia()
        self.checkall.set(False)
        
    def tabDeleteAll(self, evt):
        filtered = list(filter(lambda x: x.checked.get(), self._LS_MEDIA_UI))
        lsId = list(map( lambda x: x.id, filtered))
        if len(lsId) > 0:        
            if messagebox.askyesno("PiepMe", "Are you sure delete all selected media?"):  
                self.deleteMediaItem(lsId)
                self.tabRefresh(evt)

    def tabSelectAll(self):
        for medi in self._LS_MEDIA_UI:
            medi.checked.set(self.checkall.get())

    def showAddCamBtn(self):
        popupaddresource = PopupAddResource(self)
        imAdd = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}add-rgb24.png"))
        self.cmdAdd = tk.Label(self.tbright, image=imAdd, cursor='hand2', bg=self.tbBgColor)
        self.cmdAdd.image = imAdd
        self.cmdAdd.bind("<Button-1>", popupaddresource.initGUI)
        self.cmdAdd.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(self.cmdAdd, "Add new media")

    def addMediaToList(self, media):
        pass

    def showLsMedia(self):
        self._LS_MEDIA_DATA = self.loadLsMedia()
        if bool(self._LS_MEDIA_DATA):
            for media in self._LS_MEDIA_DATA:
                self.addMediaToList(media)
                if self.tabType == MediaType.SCHEDULE:
                    self.totalDuration += int(media['duration'])

    def clearData(self, clearView=False):
        self._LS_MEDIA_DATA = []
        self.writeLsMedia([])
        if clearView:
            self.clearView()
    
    def clearView(self):
        self._LS_MEDIA_UI = []

    def renewData(self, lsMedia):
        self.clearData(clearView=True)
        lsMedia = list(map(lambda l500: {
                    "id":  str(l500['_id']) or '',
                    "name": l500['LV501'] or '',
                    "url": l500['LV506'],
                    "rtmp": l500['LV507'],
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
        elif self.tabType == MediaType.SCHEDULE:
            helper._add_to_schedule(data)

    def loadLsMedia(self):
        if self.tabType == MediaType.CAMERA:
            return helper._load_lscam()
        elif self.tabType == MediaType.IMAGE:
            return helper._load_image()
        elif self.tabType == MediaType.VIDEO:
            return helper._load_video()
        elif self.tabType == MediaType.PRESENTER:
            return helper._load_ls_presenter()
        elif self.tabType == MediaType.SCHEDULE:
            return helper._load_schedule()

    def writeLsMedia(self, data):
        if self.tabType == MediaType.CAMERA:
            helper._write_lscam(data)
        elif self.tabType == MediaType.IMAGE:
            helper._write_image(data)
        elif self.tabType == MediaType.VIDEO:
            helper._write_video(data)
        elif self.tabType == MediaType.PRESENTER:
           helper._write_lspresenter(data)
        elif self.tabType == MediaType.SCHEDULE:
            helper._write_schedule(data)

    def deleteMediaItem(self, lsId):
        ls = self.loadLsMedia()
        filtered = list(filter(lambda x:x['id'] not in lsId, ls))
        self.clearData()
        self.writeLsMedia(filtered)

