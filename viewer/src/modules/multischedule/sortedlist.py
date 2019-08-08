import tkinter as tk
from tkinter import ttk
from .scheduleddlist import ScheduleDDList
from src.modules.custom import DDList
from src.utils import helper
from src.modules.custom import ToolTip
from PIL import Image, ImageTk
from src.modules.mediaitem import ScheduleHeadItem, ScheduleHeadItemEdit


class SortedList(ScheduleDDList):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.tbBgColor = '#E8DAEF'
        self.wrapperWidth = 300
        super(SortedList, self).__init__(parent, *args, **kwargs)
        self.titleTxt = 'Schedule List'
        self.initUI()
        

    def initUI(self):
        super(SortedList, self).initUI()
        self.showListSchedule()

    def showListSchedule(self):
        #1. default
        self.addToScheduleGUI({
            "path": "",
            "id": "STORE_SCHEDULE",
            "name": "RUNNING SCHEDULE"
        })
         #2. list
        self._LS_SCHEDULE_DATA = self.loadSchedule()
        for media in self._LS_SCHEDULE_DATA:
            self.addToScheduleGUI(media)

    def packRightToolbar(self):
        super(SortedList, self).packRightToolbar()
        # add
        self.showAddCamBtn()

    def addToScheduleGUI(self, data):
        item = self.ddlist.create_item(value=data)
        ui = ScheduleHeadItem(item, parentTab=self, media=data)
        self._LS_SCHEDULE_UI.append(ui)
        ui.pack(expand=True)
        self.ddlist.add_item(item)

    def showAddCamBtn(self):
        imAdd = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}add-rgb24.png"))
        self.cmdAdd = tk.Label(self.tbright, image=imAdd, cursor='hand2', bg=self.tbBgColor)
        self.cmdAdd.image = imAdd
        self.cmdAdd.bind("<Button-1>", self.createSchedule)
        self.cmdAdd.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(self.cmdAdd, "Create schedule")

    def createSchedule(self, evt):
        editableFiltered = list(filter(lambda ui: isinstance(ui, ScheduleHeadItemEdit), self._LS_SCHEDULE_UI))
        if 0 == len(editableFiltered):# no one element edit able
            item = self.ddlist.create_item(value={})
            ui = ScheduleHeadItemEdit(item, parentTab=self)
            self._LS_SCHEDULE_UI.append(ui)
            ui.pack(expand=True)
            self.ddlist.add_item(item)

    def loadScheduleDE(self, sch):
        self.clearScheduleActived()
        self.parent.schedule.setData(sch)
        self.parent.schedule.showListSchedule()
    
    def clearScheduleActived(self):
        for sch in self._LS_SCHEDULE_UI:
            if sch.actived:
                sch.changeBgFollowActivation()

    def rmvSchedule(self, lsId):
        ls = self.loadSchedule()
        # saved rest
        restFiltered = list(filter(lambda x:x['id'] not in lsId, ls))
        self.clearData()
        self.writeSchedule(restFiltered)
        # rmv all file not belong in sorted list
        rmvFitered = list(filter(lambda x:x['id'] in lsId, ls))
        for sch in rmvFitered:
            self.deleteScheduleContainer(sch)

    def saveSchedule(self, sch):
        ls = self.loadSchedule()
        # check edit
        filtered = list(filter(lambda x: x['id'] == sch['id'], ls))
        if len(filtered) > 0:
            self.saveEdit(ls, sch)
        elif self.newScheduleContainer(sch):# create
            self.addToScheduleGUI(sch)
            self.addSchedule(sch)
        else:
            pass # alert somethings when create failed: dupplicate name,..
        #
        self.f5(None)

    def saveEdit(self, ls, sch):
        newLs = list(map(lambda x: sch if x['id'] == sch['id'] else x, ls))
        self.clearData()
        self.writeSchedule(newLs)

    def loadSchedule(self):
        return helper._load_sorted_schedule()

    def addSchedule(self, data):
        helper._add_to_sorted_schedule(data)

    def writeSchedule(self, data):
        helper._write_sorted_schedule(data)

    def deleteScheduleContainer(self, sch):
        helper.delete_schedule_container(sch['path'])

    def newScheduleContainer(self, sch):
        return helper.new_schedule_container(sch['path'])

    def duplicateScheduleContainer(self, sch):
        helper.duplicate_schedule_container(sch['path'])
