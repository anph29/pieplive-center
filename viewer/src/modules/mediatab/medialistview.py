import tkinter as tk
from tkinter import messagebox
from src.modules.custom import DDList
from .mediatab import MediaTab
from src.modules.mediaitem import MediaItemDnD
import PIL
from PIL import ImageTk, Image
from src.utils import helper, scryto, store
from src.modules.custom import VerticalScrolledFrame, ToolTip
from src.enums import MediaType
from src.modules.popup import PopupEditResource


class MediaListView(MediaTab):
    def __init__(self, parent, *args, **kwargs):
        self.tabType = kwargs["tabType"]
        del kwargs["tabType"]
        if "schedule" in (kwargs):
            self.schedule = kwargs["schedule"]
            del kwargs["schedule"]

        super(MediaListView, self).__init__(parent, *args, **kwargs)
        self.tbBgColor = "#F9EBEA" if self.tabType == MediaType.SCHEDULE else "#D5DBDB"
        self.parent = parent
        self.scrollZ = VerticalScrolledFrame(self, style="scroll.TFrame")
        self.ddlist = self.makeDDList(self.scrollZ.interior)
        self.ddlist.setLock(self.getLock())
        self.initUI()

    def makeDDList(self, ref):
        return DDList(
            ref,
            400,
            42,
            offset_x=5,
            offset_y=5,
            gap=5,
            item_borderwidth=1,
            item_relief=tk.FLAT,
            borderwidth=0,
            bg="#fff",
            droppedCallback=self.saveSortedList,
        )

    def initUI(self):
        super(MediaListView, self).initUI()
        if self.tabType not in (
            MediaType.CAMERA,
            MediaType.PRESENTER,
            MediaType.SCHEDULE,
        ):
            self.showAddCamBtn()
        #
        self.scrollZ.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ddlist.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def packLeftToolbar(self):
        super(MediaListView, self).packLeftToolbar()
        self.checkbox.destroy()
        self.showSelectAll()

    def packRightToolbar(self):
        super(MediaListView, self).packRightToolbar()
        if self.tabType not in [MediaType.SCHEDULE, MediaType.AUDIO]:
            self.showBtnPushAllToSchedule()

    def addMediaToList(self, media):
        item = self.ddlist.create_item(value=media)
        ui = MediaItemDnD(item, parentTab=self, media=media)
        self._LS_MEDIA_UI.append(ui)
        ui.pack(expand=True)
        self.ddlist.add_item(item)

    # push all to schedule
    def showBtnPushAllToSchedule(self):
        imgPush = ImageTk.PhotoImage(
            Image.open(f"{helper._ICONS_PATH}push-all-sch.png")
        )
        self.cmdPush = tk.Label(
            self.tbright, image=imgPush, cursor="hand2", bg=self.tbBgColor
        )
        self.cmdPush.image = imgPush
        self.cmdPush.bind("<Button-1>", self.pushAllToSchedule)
        self.cmdPush.pack(side=tk.RIGHT, padx=(5, 0))
        ToolTip(self.cmdPush, "Push all selected to schedule")

    def clearView(self):
        super(MediaListView, self).clearView()
        self.ddlist._clear_all()

    def saveSortedList(self):
        sorted = list(map(lambda x: x.value, self.ddlist._list_of_items))
        filtered = list(filter(lambda x: bool(x), sorted))
        self.clearData()
        self.writeLsMedia(filtered)

    def showPopupAddSchedule(self, data):
        if self.schedule.notWarningLocked():
            self.schedule.showAddToSchedulePopup(data)

    def mergeAudioToSchedule(self, data):
        self.schedule.mergeAudioToSchedule(data)

    def pushAllToSchedule(self, evt):
        filtered = list(filter(lambda x: x.checked.get(), self._LS_MEDIA_UI))
        mapped = list(map(lambda x: x.get_data(), filtered))
        if (
            len(mapped) > 0
            and self.schedule.notWarningLocked()
            and messagebox.askyesno(
                "PiepMe", "Are you sure push all selected media to schedule?"
            )
        ):
            for medi in mapped:
                # need new id any time
                medi["id"] = scryto.hash_md5_with_time(medi["url"])
                self.schedule.saveToSchedule(medi)

    def showEditMedia(self, data):
        if self.notWarningLocked():
            editMedia = PopupEditResource(self, data)
            editMedia.initGUI(data)

    def saveToMediaList(self, media):
        ls = self.loadLsMedia()
        filtered = list(filter(lambda x: x["id"] == media["id"], ls))
        if len(filtered) > 0:
            newLs = list(map(lambda x: media if x["id"] == media["id"] else x, ls))
            self.clearData()
            self.writeLsMedia(newLs)
        self.f5(None)

    def stopAllAudio(self):
        for medi in self._LS_MEDIA_UI:
            if medi.playing_audio:
                medi.triggerStop()

