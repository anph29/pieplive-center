import tkinter as tk
from src.modules.custom import DDList
from src.modules.mediaitem import MediaItemSchedule
from .medialistview import MediaListView
from src.enums import MediaType
from src.modules.addresource import PopupAddSchedule

class MediaScheduleView(MediaListView):
    def __init__(self, parent, *args, **kwargs):
        super(MediaScheduleView, self).__init__(parent, *args, **kwargs)

    def makeDDList(self, ref):
        return DDList(ref, 
            600,
            50,
            offset_x=5,
            offset_y=5,
            gap=5,
            item_borderwidth=1,
            item_relief=tk.FLAT,
            borderwidth=0,
            bg="#fff")

    def initUI(self):
        super(MediaListView, self).initUI()
        self.showCmdSaveSortedMediaLst()
        if self.tabType == MediaType.IMAGE or self.tabType == MediaType.VIDEO:
            self.showAddCamBtn()
        #
        self.scrollZ.pack(fill=tk.BOTH, expand=True)
        self.ddlist.pack(fill=tk.Y, expand=True)

    def addMediaToList(self, media):
        item = self.ddlist.create_item(value=media)
        medi = MediaItemSchedule(item, parentTab=self, media=media)
        medi.pack(padx= (4,0), pady= (4,0), expand=True)
        self.ddlist.add_item(item)

    def showAddToSchedulePopup(self, data, edit=False):
        addresource = PopupAddSchedule(self, data)
        addresource.initGUI(edit=edit)

    def saveToSchedule(self, data):
        # check edit
        ls = self.loadLsMedia()
        filtered = list(filter(lambda x:x['id'] == data['id'], ls))
        if len(filtered) > 0:
            self.saveEdit(ls, data)
        else:
            self.addMediaToList(data)
            self.addMedia(data)

    def saveEdit(self, ls, media):
        newLs = list(map(lambda x: media if x['id'] == media['id'] else x, ls))
        self.clearData()
        self.writeLsMedia(newLs)
        self.tabRefresh(None)