import tkinter as tk
from .scheduleddlist import ScheduleDDList
from src.modules.custom import DDList
from src.utils import helper
from src.modules.mediaitem import MediaItemSchedule


class SingleSchedule(ScheduleDDList):

    def __init__(self, parent, *args, **kwargs):
        self.tbBgColor = '#D4EFDF'
        super(SingleSchedule, self).__init__(parent, *args, **kwargs)
        self.initUI()

    def setData(self, sch):
        self.schName = sch['name'] if bool(sch) else ''
        self.schId = sch['id'] if bool(sch) else ''
        self.schPath = sch['path'] if bool(sch) else ''

    def initUI(self, data=None):
        self.setData(data)
        if bool(self.schId):
            self.showListSchedule()
        self.showToolBar()
        #
        self.scrollZ.pack(fill=tk.BOTH, expand=True)
        self.ddlist.pack(fill=tk.Y, expand=True)

    def makeDDList(self, ref):
        return DDList(ref, 600, 42, offset_x=5, offset_y=5, gap=5, item_borderwidth=1, item_relief=tk.FLAT, borderwidth=0, bg="#fff", droppedCallback=self.saveSortedList)

    
    def addToScheduleGUI(self, media):
        item = self.ddlist.create_item(value=media, bg='#ddd')
        ui = MediaItemSchedule(item, parentTab=self, media=media)
        self._LS_MEDIA_UI.append(ui)
        ui.pack(padx= (4,0), pady= (4,0), expand=True)
        self.ddlist.add_item(item)

    def loadSchedule(self):
        return helper._load_schedule_width_name(self.schName)

    def addSchedule(self, data):
        helper._add_to_schedule_width_name(self.schName, data)

    def writeSchedule(self, data):
        helper._write_schedule_width_name(self.schName, data)

    # list_all_schedule
    # new_schedule_container
    # delete_schedule_container
    # rename_schedule_container
    # duplicate_schedule_container
