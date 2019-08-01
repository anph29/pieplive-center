import tkinter as tk
from .scheduleddlist import ScheduleDDList
from src.modules.custom import DDList
from src.utils import helper
from src.modules.custom import ToolTip
from PIL import Image, ImageTk
from src.modules.mediaitem import ScheduleHeadItem


class SortedList(ScheduleDDList):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.tbBgColor = '#E8DAEF'
        self.wrapperWidth = 320
        super(SortedList, self).__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        super(SortedList, self).initUI()
        self.showListSchedule()

    def packRightToolbar(self):
        super(SortedList, self).packRightToolbar()
        # add
        self.showAddCamBtn()

    def addToScheduleGUI(self, data):
        item = self.ddlist.create_item(value=data)
        ui = ScheduleHeadItem(item, parentTab=self, media=data)
        self._LS_SCHEDULE_UI.append(ui)
        ui.pack(padx=(4, 0), pady=(4, 0), expand=True)
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

    def loadScheduleDE(self, sch):
        self.parent.schedule.setData(sch)
        self.parent.schedule.showListSchedule()

    def editSchedule(self, sch):
        pass

    def loadSchedule(self):
        return helper._load_sorted_schedule()

    def addSchedule(self, data):
        helper._add_to_sorted_schedule(data)

    def writeSchedule(self, data):
        helper._write_sorted_schedule(data)
