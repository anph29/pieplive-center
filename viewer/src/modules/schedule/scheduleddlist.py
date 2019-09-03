import tkinter as tk
from tkinter import messagebox
from src.modules.custom import DDList, VerticalScrolledFrame
from src.utils import helper, store
from src.modules.custom import ToolTip
from PIL import Image, ImageTk
from src.constants import UI, STORE_SCHEDULE


class ScheduleDDList(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(ScheduleDDList, self).__init__(parent, *args, **kwargs)
        self._LS_SCHEDULE_DATA = []
        self._LS_SCHEDULE_UI = []
        self.titleTxt = ""
        self.tbBgColor = "#fff"
        self.wrapperWidth = 0
        self.keyLock = None

    def initUI(self):
        self.showToolBar()
        self.showTitle()
        #
        self.scrollZ = VerticalScrolledFrame(self)
        self.scrollZ.pack(fill=tk.BOTH, expand=True)
        #
        self.ddlist = self.makeDDList(self.scrollZ.interior)
        self.ddlist.setLock(self.getLock())
        self.ddlist.pack(fill=tk.BOTH, expand=True)

    def showTitle(self):
        self.title = tk.Frame(self, height=50, relief=tk.FLAT, bg=self.tbBgColor)
        self.title.pack(fil=tk.X, side=tk.TOP)
        #
        self.lblTitle = tk.Label(
            self.title,
            text=self.titleTxt.upper(),
            bg=self.tbBgColor,
            font=UI.TITLE_FONT,
        )
        self.lblTitle.pack(pady=5)

    def makeDDList(self, ref):
        return DDList(
            ref,
            self.wrapperWidth,
            42,
            offset_x=5,
            offset_y=5,
            gap=5,
            item_borderwidth=1,
            item_relief=tk.FLAT,
            borderwidth=0,
            bg="#fff",
            droppedCallback=self.saveSortedList,
        )

    def loadSchedule(self):
        return []

    def addToScheduleGUI(self, media):
        pass

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
        self.checkbox = tk.Checkbutton(
            self.tbleft,
            variable=self.checkall,
            onvalue=True,
            offvalue=False,
            height=2,
            width=2,
            bg=self.tbBgColor,
            bd=0,
            cursor="hand2",
            command=self.tabSelectAll,
        )
        self.checkbox.pack(side=tk.LEFT, fill=tk.Y)
        ToolTip(self.checkbox, "Select all media")

    def packRightToolbar(self):
        self.tbright = tk.Frame(self.toolbar, relief=tk.FLAT, bg=self.tbBgColor)
        self.tbright.pack(fil=tk.Y, side=tk.RIGHT)
        # delete all
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b24.png"))
        self.cmdDelAll = tk.Label(
            self.tbright, image=imageBin, cursor="hand2", bg=self.tbBgColor
        )
        self.cmdDelAll.image = imageBin
        self.cmdDelAll.bind("<Button-1>", self.tabDeleteAll)
        self.cmdDelAll.pack(side=tk.RIGHT, padx=(0, 15), pady=5)
        ToolTip(self.cmdDelAll, "Delete all selected")
        # refresh
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}f5-b24.png"))
        self.cmdF5 = tk.Label(
            self.tbright, image=imageBin, cursor="hand2", bg=self.tbBgColor
        )
        self.cmdF5.image = imageBin
        self.cmdF5.bind("<Button-1>", self.f5)
        self.cmdF5.pack(side=tk.RIGHT, padx=(0, 5), pady=5)
        ToolTip(self.cmdF5, "Refresh")
        # lock
        un = "" if self.getLock() else "un"
        imgLock = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}{un}lock-24.png"))
        self.cmdLock = tk.Label(
            self.tbright, image=imgLock, cursor="hand2", bg=self.tbBgColor
        )
        self.cmdLock.image = imgLock
        self.cmdLock.bind("<Button-1>", self.toggleLock)
        self.cmdLock.pack(side=tk.RIGHT, padx=(0, 5))
        ToolTip(self.cmdLock, "unlocked")

    def toggleLock(self, evt):
        un = "un" if self.getLock() else ""
        imgLock = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}{un}lock-24.png"))
        self.cmdLock.configure(image=imgLock)
        self.cmdLock.image = imgLock
        ToolTip(self.cmdLock, f"{un}locked")
        #
        locked = not self.ddlist.getLock()
        self.ddlist.setLock(locked)
        self.setLock(locked)

    def setLock(self, locked):
        return store._set(self.keyLock, locked)

    def getLock(self):
        return bool(store._get(self.keyLock))

    def f5(self, evt):
        self.clearView()
        self.showListSchedule()
        self.checkall.set(False)

    def tabDeleteAll(self, evt):
        filtered = list(filter(lambda x: x.checked.get(), self._LS_SCHEDULE_UI))
        lsId = list(map(lambda x: x.id, filtered))
        if len(lsId) > 0:
            if messagebox.askyesno(
                "PiepMe", "Are you sure delete all selected schedule?"
            ):
                self.rmvSchedule(lsId)
                self.f5(evt)

    def tabSelectAll(self):
        for medi in self._LS_SCHEDULE_UI:
            medi.checked.set(self.checkall.get())

    def clearData(self, clearView=False):
        # self._LS_SCHEDULE_DATA = []
        self.writeSchedule([])
        if clearView:
            self.clearView()

    def clearView(self):
        self._LS_SCHEDULE_UI = []
        self.ddlist._clear_all()

    def rmvSchedule(self, lsId):
        ls = self.loadSchedule()
        filtered = list(filter(lambda x: x["id"] not in lsId, ls))
        self.clearData()
        self.writeSchedule(filtered)

    def saveSortedList(self):
        sorted = list(map(lambda x: x.value, self.ddlist._list_of_items))
        filtered = list(
            filter(lambda x: bool(x) and x["id"] != STORE_SCHEDULE, sorted)
        )
        # index, timepoint = self.get1stEvalueTimepoint(sorted)
        self.clearData()
        self.writeSchedule(filtered)

    def showListSchedule(self):
        pass

    def writeSchedule(self, data):
        pass

    # def get1stEvalueTimepoint(self, ls):
    #     for i, m in enumerate(ls):
    #         if 'timepoint' in m and int(m['timepoint']) > 0:
    #             return i, m['timepoint']
