import tkinter as tk
from src.utils import store
from src.constants import WS, UI
from src.models import P300_model
from src.modules.comitem import P300
from src.modules.custom import DynamicGrid
from src.modules.custom import ToolTip
from PIL import Image, ImageTk
from src.utils import helper


class ListP300(DynamicGrid, tk.Frame):
    def __init__(self, parent, keyManager=None, *args, **kwargs):
        super(ListP300, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.keyManager = keyManager
        self.tbBgColor = "#E8DAEF"
        self._LS_P300_DATA = []
        self._LS_P300_UI = []
        self.initUI()

    def initUI(self):
        self.showListP300()
        self.showToolBar()

    def showToolBar(self):
        self.checkall = tk.BooleanVar()
        self.toolbar = tk.Frame(self, height=50, relief=tk.FLAT, bg=self.tbBgColor)
        self.toolbar.pack(fil=tk.X, side=tk.BOTTOM)
        # refresh
        imF5 = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}f5-b24.png"))
        self.cmdF5 = tk.Label(
            self.toolbar, image=imF5, cursor="hand2", bg=self.tbBgColor
        )
        self.cmdF5.image = imF5
        self.cmdF5.bind("<Button-1>", self.f5)
        self.cmdF5.pack(side=tk.RIGHT, padx=(0, 5), pady=5)
        ToolTip(self.cmdF5, "Refresh")

    def showListP300(self):
        self._LS_P300_DATA = self.loadListP300COM()
        for media in self._LS_P300_DATA:
            self.addItemToGUI(media)

    def addItemToGUI(self, p300):
        ui = P300(self.context, p300, parentTab=self, bg="#fff", relief=tk.FLAT, bd=3)
        self._LS_P300_UI.append(ui)
        self.after_effect(ui)

    def clearView(self):
        self.context.config(state=tk.NORMAL)
        self.context.delete(1.0, tk.END)
        self.context.config(state=tk.DISABLED)

    def loadListP300COM(self):
        p300 = P300_model()
        rs = p300.listoftabP300EByOwner(
            {
                "ACTION": "SENT",
                "PP300": 0,
                "FO100": store.getCurrentActiveBusiness(),  # chủ doanh nghiệp
                "FO100W": store._get("FO100"),  # người viết
                "SEARCH": "",
                "OFFSET": 0,
                "LIMIT": 30,
                "LOGIN": store._get("NV101"),
                "FILTER": ["LIVE", "COUNTDOWN"],  # Chỉ dành cho App Pieplivecenter
            }
        )
        return rs[WS.ELEMENTS] if rs[WS.STATUS] == WS.SUCCESS else []

    def canInsertL300(self, PP300):
        return self.keyManager.notkExistedKey(PP300)

    def saveKeyStream(self, keyObj):
        self.keyManager.addKey(keyObj)

    def f5(self, evt):
        self.clearView()
        self.showListP300()
