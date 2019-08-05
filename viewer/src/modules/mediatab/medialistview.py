import tkinter as tk
from tkinter import messagebox
from src.modules.custom import DDList
from .mediatab import MediaTab
from src.modules.mediaitem import MediaItemDnD
import PIL
from PIL import ImageTk, Image
from src.utils import helper, scryto
from src.modules.custom import VerticalScrolledFrame, ToolTip
from src.enums import MediaType
from src.modules.popup import PopupEditResource


class MediaListView(MediaTab):
    def __init__(self, parent, *args, **kwargs):
        self.tabType = kwargs['tabType']
        del kwargs['tabType']
        if 'schedule' in (kwargs):
            self.schedule = kwargs['schedule']
            del kwargs['schedule']

        super(MediaListView, self).__init__(parent, *args, **kwargs)
        self.tbBgColor = '#F9EBEA' if self.tabType == MediaType.SCHEDULE else '#D5DBDB'
        self.parent = parent
        self.scrollZ = VerticalScrolledFrame(self, style='scroll.TFrame')
        self.ddlist = self.makeDDList(self.scrollZ.interior)
        self.initUI()

    def makeDDList(self, ref):
        return DDList(ref, 400, 42, offset_x=5, offset_y=5, gap=5, item_borderwidth=1, item_relief=tk.FLAT, borderwidth=0, bg="#fff", droppedCallback=self.saveSortedList)

    def initUI(self):
        super(MediaListView, self).initUI()
        if self.tabType == MediaType.IMAGE or self.tabType == MediaType.VIDEO:
            self.showAddCamBtn()
        #
        self.scrollZ.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ddlist.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def packLeftToolbar(self):
        super(MediaListView, self).packLeftToolbar()
        self.checkbox.destroy()
        if self.tabType != MediaType.SCHEDULE:
            self.showBtnPushAllToSchedule()
        self.showSelectAll()

    def addMediaToList(self, media):
        item = self.ddlist.create_item(value=media)
        ui = MediaItemDnD(item, parentTab=self, media=media)
        self._LS_MEDIA_UI.append(ui)
        ui.pack(expand=True)
        self.ddlist.add_item(item)

    def showBtnPushAllToSchedule(self):
        # push to schedule
        imgPush = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}push-left.png"))
        lblPush = tk.Label(self.tbleft, image=imgPush, cursor='hand2', bg=self.tbBgColor)
        lblPush.image = imgPush
        lblPush.bind("<Button-1>", self.pushAllToSchedule)
        lblPush.pack(side=tk.LEFT, padx=(5, 0))

    def clearView(self):
        super(MediaListView, self).clearView()
        self.ddlist._clear_all()

    def saveSortedList(self):
        sorted = list(map(lambda x: x.value, self.ddlist._list_of_items))
        filtered = list(filter(lambda x:bool(x), sorted))
        self.clearData()
        self.writeLsMedia(filtered)

    def callShowPopup(self, data):
        self.schedule.showAddToSchedulePopup(data)

    def pushAllToSchedule(self, evt):
        filtered = list(filter(lambda x: x.checked.get(), self._LS_MEDIA_UI))
        mapped = list(map(lambda x: x.get_data(), filtered))
        if len(mapped) > 0:
            if messagebox.askyesno("PiepMe", "Are you sure push all selected media to schedule?"):
                for medi in mapped:
                    # need new id any time
                    medi['id'] = scryto.hash_md5_with_time(medi['url'])
                    self.schedule.saveToSchedule(medi)

    def showEditMedia(self, data):
        editMedia = PopupEditResource(self, data)
        editMedia.initGUI(data)

    def saveToMediaList(self, media):
        ls = self.loadLsMedia()
        filtered = list(filter(lambda x: x['id'] == media['id'], ls))
        if len(filtered) > 0:
            newLs = list(
                map(lambda x: media if x['id'] == media['id'] else x, ls))
            self.clearData()
            self.writeLsMedia(newLs)
        self.f5(None)
