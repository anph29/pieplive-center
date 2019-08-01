import tkinter as tk
from tkinter import messagebox
from src.modules.custom import DDList
from src.modules.mediaitem import MediaItemSchedule
from .medialistview import MediaListView
from src.enums import MediaType
from src.modules.popup import PopupAddSchedule
from src.utils import helper
from functools import reduce
from src.constants import UI

class MediaScheduleView(MediaListView):
    def __init__(self, parent, *args, **kwargs):
        super(MediaScheduleView, self).__init__(parent, *args, **kwargs)

    def makeDDList(self, ref):
        return DDList(ref, 820, 42, offset_x=5, offset_y=5, gap=5, item_borderwidth=1, item_relief=tk.FLAT, borderwidth=0, bg="#fff", droppedCallback=self.saveSortedList)

    def initUI(self):
        super(MediaScheduleView, self).initUI()
        #
        self.scrollZ.pack(fill=tk.BOTH, expand=True)
        self.ddlist.pack(fill=tk.Y, expand=True)

    def packRightToolbar(self):
        super(MediaScheduleView, self).packRightToolbar()
        # label
        self.lblDura = tk.Label(self.tbright, text=f'total duration: {helper.convertSecNoToHMS(self.totalDuration)}', justify=tk.LEFT, bg=self.tbBgColor, font=UI.TXT_FONT_HEAD, fg="#ff2d55")
        self.lblDura.pack(side=tk.RIGHT, padx=10)

    def addMediaToList(self, media):
        item = self.ddlist.create_item(value=media, bg='#ddd')
        ui = MediaItemSchedule(item, parentTab=self, media=media)
        self._LS_MEDIA_UI.append(ui)
        ui.pack(padx= (4,0), pady= (4,0), expand=True)
        self.ddlist.add_item(item)

    def showAddToSchedulePopup(self, data, edit=False):
        addresource = PopupAddSchedule(self, data)
        addresource.initGUI(edit=edit)

    def editRuntime(self, data):
        addresource = PopupAddSchedule(self, data)
        addresource.showChangeRuntimeUI()
    
    def saveToSchedule(self, data):
        ls = self.loadLsMedia()
        # check edit
        filtered = list(filter(lambda x:x['id'] == data['id'], ls))
        if len(filtered) > 0:
            self.saveEdit(ls, data)
        else:
            self.addMediaToList(data)
            self.addMedia(data)
        self.f5(None)

    def f5(self, evt):
        super(MediaScheduleView, self).f5(evt)
        ls = self.loadLsMedia()
        self.totalDuration = reduce(lambda sum, x: sum + x['duration'], ls, 0)
        self.lblDura.config(text=f'total duration: {helper.convertSecNoToHMS(self.totalDuration)}')

    def saveEdit(self, ls, media):
        newLs = list(map(lambda x: media if x['id'] == media['id'] else x, ls))
        self.clearData()
        self.writeLsMedia(newLs)

    def calcRuntime(self, media):
        ls = self.loadLsMedia()
        newLs = list(map(lambda x: media if x['id'] == media['id'] else x, ls))
        index = newLs.index(media)
        self.clearData()
        schedule = helper.calc_schedule_runtime(index, schedule=newLs, startTime=media['timepoint'])
        self.writeLsMedia(schedule)
        self.f5(None)

    def saveSortedList(self):
        sorted = list(map(lambda x:x.value, self.ddlist._list_of_items))
        # index, timepoint = self.get1stEvalueTimepoint(sorted)
        self.clearData()
        self.writeLsMedia(sorted)

    # def get1stEvalueTimepoint(self, ls):
    #     for i, m in enumerate(ls):
    #         if 'timepoint' in m and int(m['timepoint']) > 0:
    #             return i, m['timepoint']