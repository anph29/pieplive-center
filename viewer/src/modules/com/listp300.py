import tkinter as tk
from src.utils import store
from src.constants import WS, UI
from src.models import P300_model
from src.modules.comitem import P300
from src.modules.custom import DynamicGrid


class ListP300(DynamicGrid, tk.Frame):
    def __init__(self, parent, keyManager=None, *args, **kwargs):
        super(ListP300, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.keyManager = keyManager
        self.tbBgColor = "#E8DAEF"
        self.titleTxt = "Schedule List"
        self._LS_P300_DATA = []
        self._LS_P300_UI = []
        self.initUI()

    def initUI(self):
        self.showListSchedule()

    def showListSchedule(self):
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

    def saveKeyStream(self, keyObj):
        self.keyManager.addKey(keyObj)
