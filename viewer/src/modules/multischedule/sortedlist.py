import tkinter as tk
from .scheduleddlist import ScheduleDDList
from src.modules.custom import DDList
from src.utils import helper
from src.modules.custom import ToolTip
from PIL import Image, ImageTk
from src.modules.mediaitem import ScheduleHeadItem


class SortedList(ScheduleDDList):

    def __init__(self, parent, *args, **kwargs):
        self.tbBgColor = '#E8DAEF'
        super(SortedList, self).__init__(parent, *args, **kwargs)
        self.initUI()

    def makeDDList(self, ref):
        return DDList(ref, 360, 42, offset_x=5, offset_y=5, gap=5, item_borderwidth=1, item_relief=tk.FLAT, borderwidth=0, bg="#fff", droppedCallback=self.saveSortedList)

    def initUI(self):
        self.showListSchedule()
        self.showToolBar()
        #
        self.scrollZ.pack(fill=tk.BOTH, expand=True)
        self.ddlist.pack(fill=tk.Y, expand=True)

    def packRightToolbar(self):
        super(SortedList, self).packRightToolbar()
        # add
        self.showAddCamBtn()

    def addToScheduleGUI(self, data):
        item = self.ddlist.create_item(value=data)
        ui = ScheduleHeadItem(item, parentTab=self, media=data)
        self._LS_SCHEDULE_UI.append(ui)
        ui.pack(padx= (4,0), pady= (4,0), expand=True)
        self.ddlist.add_item(item)

    def showAddCamBtn(self):
        # popupaddresource = PopupAddResource(self)
        imAdd = ImageTk.PhotoImage(Image.open(
            f"{helper._ICONS_PATH}add-rgb24.png"))
        self.cmdAdd = tk.Label(self.tbright, image=imAdd,
                               cursor='hand2', bg=self.tbBgColor)
        self.cmdAdd.image = imAdd
        # self.cmdAdd.bind("<Button-1>", popupaddresource.initGUI)
        self.cmdAdd.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(self.cmdAdd, "Add new media")

    def loadSchedule(self):                                              
            return helper._load_sorted_schedule()

    def addSchedule(self, data):
            helper._add_to_sorted_schedule(data)

    def writeSchedule(self, data):
            helper._write_sorted_schedule(data)