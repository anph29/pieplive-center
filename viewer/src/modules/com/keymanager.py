import tkinter as tk
from tkinter import messagebox
from src.modules.custom import DDList, VerticalScrolledFrame
from src.utils import helper
from src.modules.comitem import Key
from functools import reduce
from src.constants import UI
from PIL import Image, ImageTk
from src.modules.custom import ToolTip
from src.modules.popup import PopupAddKey


class KeyManager(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(KeyManager, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self._LS_KEY_DATA = []
        self._LS_KEY_UI = []
        self.tbBgColor = "#D4EFDF"
        self.wrapperWidth = 360
        self.titleTxt = "Key manager"
        self.initUI()
        self.lblChk = None

    def initUI(self):
        self.showTitle()
        self.showToolBar()
        self.scrollZ = VerticalScrolledFrame(self)
        self.scrollZ.pack(fill=tk.BOTH, expand=True)
        self.ddlist = self.makeDDList(self.scrollZ.interior)
        self.ddlist.pack(fill=tk.BOTH, expand=True)
        self.showListKey()

    def showListKey(self):
        self._LS_KEY_DATA = helper._load_ls_key()
        if bool(self._LS_KEY_DATA):
            for key in self._LS_KEY_DATA:
                self.addToKeyGUI(key)

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

    def addToKeyGUI(self, key):
        item = self.ddlist.create_item(value=key)
        ui = Key(item, parentTab=self, key=key)
        self._LS_KEY_UI.append(ui)
        ui.pack(expand=True)
        self.ddlist.add_item(item)

    def showToolBar(self):
        self.checkall = tk.BooleanVar()
        self.toolbar = tk.Frame(self, height=50, relief=tk.FLAT, bg=self.tbBgColor)
        self.toolbar.pack(fil=tk.X, side=tk.BOTTOM)
        self.packLeftToolbar()
        self.packRightToolbar()

    def packLeftToolbar(self):
        self.tbleft = tk.Frame(self.toolbar, relief=tk.FLAT, bg=self.tbBgColor)
        self.tbleft.pack(fil=tk.Y, side=tk.LEFT)
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
        imF5 = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}f5-b24.png"))
        self.cmdF5 = tk.Label(
            self.tbright, image=imF5, cursor="hand2", bg=self.tbBgColor
        )
        self.cmdF5.image = imF5
        self.cmdF5.bind("<Button-1>", self.f5)
        self.cmdF5.pack(side=tk.RIGHT, padx=(0, 5), pady=5)
        ToolTip(self.cmdF5, "Refresh")
        # lock
        imgLock = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}unlock-24.png"))
        self.cmdLock = tk.Label(
            self.tbright, image=imgLock, cursor="hand2", bg=self.tbBgColor
        )
        self.cmdLock.image = imgLock
        self.cmdLock.bind("<Button-1>", self.toggleLock)
        self.cmdLock.pack(side=tk.RIGHT, padx=(0, 5))
        ToolTip(self.cmdLock, "unlocked")
        # ADD
        imAdd = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}add-rgb24.png"))
        self.cmdAdd = tk.Label(
            self.tbright, image=imAdd, cursor="hand2", bg=self.tbBgColor
        )
        self.cmdAdd.image = imAdd
        self.cmdAdd.bind("<Button-1>", self.showAddKey)
        self.cmdAdd.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(self.cmdAdd, "Add new key")

    def showAddKey(self, evt):
        popupAddKey = PopupAddKey(self)
        popupAddKey.initGUI()

    def showEditKey(self, key):
        popupAddKey = PopupAddKey(self, data=key)
        popupAddKey.initGUI(edit=True)

    def toggleLock(self, evt):
        un = "un" if self.ddlist.getLock() else ""
        imgLock = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}{un}lock-24.png"))
        self.cmdLock.configure(image=imgLock)
        self.cmdLock.image = imgLock
        ToolTip(self.cmdLock, f"{un}locked")
        self.ddlist.setLock(not self.ddlist.getLock())

    def f5(self, evt):
        self.clearView()
        self.showListKey()
        self.checkall.set(False)

    def tabDeleteAll(self, evt):
        filtered = list(filter(lambda x: x.checked.get(), self._LS_KEY_UI))
        lsId = list(map(lambda x: x.id, filtered))
        if len(lsId) > 0:
            if messagebox.askyesno("PiepMe", "Are you sure delete all selected keys?"):
                self.rmvKey(lsId)
                self.f5(evt)

    def tabSelectAll(self):
        for medi in self._LS_KEY_UI:
            medi.checked.set(self.checkall.get())

    def clearData(self, clearView=False):
        # self._LS_KEY_DATA = []
        helper._write_lskey([])
        if clearView:
            self.clearView()

    def clearView(self):
        self._LS_KEY_UI = []
        self.ddlist._clear_all()

    def rmvKey(self, lsId):
        ls = helper._load_ls_key()
        filtered = list(filter(lambda x: x["id"] not in lsId, ls))
        self.clearData()
        helper._write_lskey(filtered)
        self.after(50, self.parent.parent.f5Left)

    def saveSortedList(self):
        sorted = list(map(lambda x: x.value, self.ddlist._list_of_items))
        filtered = list(filter(lambda x: bool(x), sorted))
        self.clearData()
        helper._write_lskey(filtered)

    def notkExistedKey(self, PP300):
        filtered = list(
            filter(
                lambda k: "PP300" in k["P300"] and k["P300"]["PP300"] == PP300,
                self._LS_KEY_DATA,
            )
        )
        return len(filtered) == 0

    def addKey(self, keyObj):
        helper._add_to_lskey(keyObj)
        self.f5(None)

    def saveEditKey(self, keyObj):
        ls = helper._load_ls_key()
        filtered = list(filter(lambda x: x["id"] == keyObj["id"], ls))
        if len(filtered) > 0:
            newLs = list(map(lambda x: keyObj if x["id"] == keyObj["id"] else x, ls))
            self.clearData()
            helper._write_lskey(newLs)

        self.f5(None)