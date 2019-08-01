import tkinter as tk
from .scheduleddlist import ScheduleDDList
from src.modules.custom import DDList
from src.utils import helper
from src.modules.mediaitem import MediaItemSchedule
from functools import reduce
from src.modules.popup import PopupAddSchedule
from src.constants import UI


class SingleSchedule(ScheduleDDList):

    def __init__(self, parent, *args, **kwargs):
        super(SingleSchedule, self).__init__(parent, *args, **kwargs)
        self.tbBgColor = '#D4EFDF'
        self.wrapperWidth = 500
        self.totalDuration = 0
        self.initUI()

    def setData(self, sch):
        self.schName = sch['name'] if bool(sch) else ''
        self.schId = sch['id'] if bool(sch) else ''
        self.schPath = sch['path'] if bool(sch) else ''

    def addToScheduleGUI(self, media):
        item = self.ddlist.create_item(value=media, bg='#ddd')
        ui = MediaItemSchedule(item, parentTab=self, media=media, elipsis=20)
        self._LS_SCHEDULE_UI.append(ui)
        ui.pack(padx=(4, 0), pady=(4, 0), expand=True)
        self.ddlist.add_item(item)

    def loadSchedule(self):
        return helper._load_schedule_width_fname(self.schPath)

    def addSchedule(self, data):
        helper._add_to_schedule_width_fname(self.schPath, data)

    def writeSchedule(self, data):
        helper._write_schedule_width_fname(self.schPath, data)

    # list_all_schedule
    # new_schedule_container
    # delete_schedule_container
    # rename_schedule_container
    # duplicate_schedule_container

    def packRightToolbar(self):
        super(SingleSchedule, self).packRightToolbar()
        # label
        self.lblDura = tk.Label(self.tbright, text=f'total duration: {helper.convertSecNoToHMS(self.totalDuration)}', justify=tk.LEFT, bg=self.tbBgColor, font=UI.TXT_FONT_HEAD, fg="#ff2d55")
        self.lblDura.pack(side=tk.RIGHT, padx=10)

    def addMediaToList(self, media):
        item = self.ddlist.create_item(value=media, bg='#ddd')
        ui = MediaItemSchedule(item, parentTab=self, media=media)
        self._LS_SCHEDULE_UI.append(ui)
        ui.pack(padx= (4,0), pady= (4,0), expand=True)
        self.ddlist.add_item(item)

    def showAddToSchedulePopup(self, data, edit=False):
        addresource = PopupAddSchedule(self, data)
        addresource.initGUI(edit=edit)

    def editRuntime(self, data):
        addresource = PopupAddSchedule(self, data)
        addresource.showChangeRuntimeUI()
    
    def saveToSchedule(self, data):
        ls = self.loadSchedule()
        # check edit
        filtered = list(filter(lambda x:x['id'] == data['id'], ls))
        if len(filtered) > 0:
            self.saveEdit(ls, data)
        else:
            self.addMediaToList(data)
            self.addSchedule(data)
        self.f5(None)

    def f5(self, evt):
        super(SingleSchedule, self).f5(evt)
        ls = self.loadSchedule()
        self.totalDuration = reduce(lambda sum, x: sum + x['duration'], ls, 0)
        self.lblDura.config(text=f'total duration: {helper.convertSecNoToHMS(self.totalDuration)}')

    def saveEdit(self, ls, media):
        newLs = list(map(lambda x: media if x['id'] == media['id'] else x, ls))
        self.clearData()
        self.writeSchedule(newLs)

    def calcRuntime(self, media):
        ls = self.loadSchedule()
        newLs = list(map(lambda x: media if x['id'] == media['id'] else x, ls))
        index = newLs.index(media)
        self.clearData()
        schedule = helper.calc_schedule_runtime(index, schedule=newLs, startTime=media['timepoint'])
        self.writeSchedule(schedule)
        self.f5(None)

    def saveSortedList(self):
        sorted = list(map(lambda x:x.value, self.ddlist._list_of_items))
        # index, timepoint = self.get1stEvalueTimepoint(sorted)
        self.clearData()
        self.writeSchedule(sorted)

    # def get1stEvalueTimepoint(self, ls):
    #     for i, m in enumerate(ls):
    #         if 'timepoint' in m and int(m['timepoint']) > 0:
    #             return i, m['timepoint']

    def deleteMediaItem(self, id):
        