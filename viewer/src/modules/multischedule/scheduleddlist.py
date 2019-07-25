import tkinter as tk
from tkinter import messagebox
from src.modules.custom import DDList, VerticalScrolledFrame
from src.utils import helper
from src.modules.custom import ToolTip
from PIL import Image, ImageTk
from src.modules.mediaitem import MediaItemSchedule


class ScheduleDDList(tk.Frame):
    def __init__(self,  parent, *args, **kwargs):
        super(ScheduleDDList, self).__init__( parent, *args, **kwargs)
        self.tbBgColor = '#fff'
        self._LS_SCHEDULE_DATA = []
        self._LS_SCHEDULE_UI = []
        self.parent = parent
        self.scrollZ = VerticalScrolledFrame(self, style='scroll.TFrame')
        self.ddlist = self.makeDDList(self.scrollZ.interior)
        self.initUI()

    def initUI(self):
        self.showListSchedule()
        self.showToolBar()

    def showListSchedule(self):
        self._LS_SCHEDULE_DATA = self.loadSchedule()
        for media in self._LS_SCHEDULE_DATA:
            self.addToScheduleGUI(media)
            # if self.tabType == MediaType.SCHEDULE:
            #     self.totalDuration += int(media['duration'])
            
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

    def addToScheduleGUI(self, data):
        item = self.ddlist.create_item(value=data)
        ui = MediaItemSchedule(item, parentTab=self, media=data)
        self._LS_SCHEDULE_UI.append(ui)
        ui.pack(padx= (4,0), pady= (4,0), expand=True)
        self.ddlist.add_item(item)
        
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
        self.cmdF5.bind("<Button-1>", self.f5)
        self.cmdF5.pack(side=tk.RIGHT, padx=(0, 5), pady=5)
        ToolTip(self.cmdF5, "Refresh")

    def f5(self, evt):
        self.clearView()
        self.showListSchedule()
        self.checkall.set(False)
        
    def tabDeleteAll(self, evt):
        filtered = list(filter(lambda x: x.checked.get(), self._LS_SCHEDULE_UI))
        lsId = list(map( lambda x: x.id, filtered))
        if len(lsId) > 0:        
            if messagebox.askyesno("PiepMe", "Are you sure delete all selected schedule?"):  
                self.rmvSchedule(lsId)
                self.f5(evt)

    def tabSelectAll(self):
        for medi in self._LS_SCHEDULE_UI:
            medi.checked.set(self.checkall.get())

    def showAddCamBtn(self):
        # popupaddresource = PopupAddResource(self)
        imAdd = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}add-rgb24.png"))
        self.cmdAdd = tk.Label(self.tbright, image=imAdd, cursor='hand2', bg=self.tbBgColor)
        self.cmdAdd.image = imAdd
        # self.cmdAdd.bind("<Button-1>", popupaddresource.initGUI)
        self.cmdAdd.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(self.cmdAdd, "Add new media")

    def clearData(self, clearView=False):
        self._LS_SCHEDULE_DATA = []
        self.writeSchedule([])
        if clearView:
            self.clearView()
    
    def clearView(self):
        self._LS_SCHEDULE_UI = []

    def addSchedule(self, data):
            helper._add_to_sorted_schedule(data)

    def loadSchedule(self):
            return helper._load_sorted_schedule()

    def writeSchedule(self, data):
            helper._write_sorted_schedule(data)

    def rmvSchedule(self, lsId):
        ls = self.loadSchedule()
        filtered = list(filter(lambda x:x['id'] not in lsId, ls))
        self.clearData()
        self.writeSchedule(filtered)
        
    def saveSortedList(self):
        print(';;;saveSortedList;;;;')