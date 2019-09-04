import tkinter as tk
from tkinter import messagebox
from .scheduleddlist import ScheduleDDList
from src.modules.custom import DDList
from src.utils import helper, store
from src.modules.mediaitem import MediaItemSchedule
from functools import reduce
from src.modules.popup import PopupAddSchedule
from src.constants import UI
from PIL import Image, ImageTk
from src.modules.custom import ToolTip


class SingleSchedule(ScheduleDDList):
    def __init__(self, parent, *args, **kwargs):
        super(SingleSchedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.tbBgColor = "#D4EFDF"
        self.wrapperWidth = 745
        self.totalDuration = 0
        self.titleTxt = "Schedule Detail"
        self.lblChk = None
        self.schId = ""
        self.isRunningSch = False
        self.schPath = ""
        self.schName = ""
        self.schLocked = False
        self.initUI()

    def showListSchedule(self):
        self._LS_SCHEDULE_DATA = self.loadSchedule()
        self.totalDuration = 0
        if bool(self._LS_SCHEDULE_DATA):
            for sch in self._LS_SCHEDULE_DATA:
                self.addToScheduleGUI(sch)
                self.totalDuration += int(sch["duration"])
        #
        self.lblDura.config(
            text=f"total duration: {helper.convertSecNoToHMS(self.totalDuration)}"
        )

    def setLock(self, locked):
        self.schLocked = locked
        # update file
        self.parent.parent.overwiteSortedItem(self.getData())

    def getLock(self):
        return self.schLocked

    def getData(self):
        return {
            "path": self.schPath,
            "id": self.schId,
            "name": self.schName,
            "lock": self.schLocked,
        }

    def setData(self, sch):
        self.schId = sch["id"] if bool(sch) else ""
        self.isRunningSch = self.schId == "STORE_SCHEDULE"
        self.schPath = sch["path"] if bool(sch) else ""
        self.schName = sch["name"] if bool(sch) else ""
        self.schLocked = sch["lock"] if bool(sch) else False
        # title
        title = f"{'RUNNING SCHEDULE: ' if self.isRunningSch else ''}{self.schName}"
        self.lblTitle.config(text=title)
        self.lblTitle.pack_forget()
        self.lblTitle.pack(side=tk.LEFT, padx=20, pady=5)
        # lock
        self.updateLockStatus("" if self.getLock() else "un")

        #
        self.showTitleWidthSave()
        self.clearView()

    def showTitleWidthSave(self):
        if self.isRunningSch:  # RUNNING
            if bool(self.lblChk):
                self.lblChk.pack_forget()
                self.lblChk = None

        elif not bool(self.lblChk):  # NORMAL
            imageChk = ImageTk.PhotoImage(
                Image.open(f"{helper._ICONS_PATH}check-green-s.png")
            )
            self.lblChk = tk.Label(
                self.title,
                image=imageChk,
                font=UI.TXT_FONT,
                cursor="hand2",
                bg=self.tbBgColor,
            )
            self.lblChk.image = imageChk
            self.lblChk.bind("<Button-1>", self.saveAsRunningSchedule)
            self.lblChk.pack(padx=35, pady=5, side=tk.RIGHT)
            ToolTip(self.lblChk, "Save as Running Schedule")

    def saveAsRunningSchedule(self, evt):
        if messagebox.askyesno("PiepMe", "Are you sure overwrite `RUNNING SCHEDULE`?"):
            helper._write_schedule(self._LS_SCHEDULE_DATA)
            store._set("RUNNING_SCHEDULE", self.schName)

    def addToScheduleGUI(self, media):
        item = self.ddlist.create_item(value=media, bg="#ddd")
        ui = MediaItemSchedule(item, parentTab=self, media=media, elipsis=50)
        self._LS_SCHEDULE_UI.append(ui)
        ui.pack(expand=True)
        self.ddlist.add_item(item)

    def loadSchedule(self):
        if self.isRunningSch:
            return helper._load_schedule()
        else:
            return helper._load_schedule_width_fname(self.schPath)

    def addSchedule(self, data):
        if self.isRunningSch:
            helper._add_to_schedule(data)
        else:
            helper._add_to_schedule_width_fname(self.schPath, data)

    def writeSchedule(self, data):
        if self.isRunningSch:
            helper._write_schedule(data)
        else:
            helper._write_schedule_width_fname(self.schPath, data)

    def packRightToolbar(self):
        super(SingleSchedule, self).packRightToolbar()
        # label
        self.lblDura = tk.Label(
            self.tbright,
            text=f"total duration: {helper.convertSecNoToHMS(self.totalDuration)}",
            justify=tk.LEFT,
            bg=self.tbBgColor,
            font=UI.TXT_FONT_HEAD,
            fg="#ff2d55",
        )
        self.lblDura.pack(side=tk.RIGHT, padx=10)

    def addMediaToList(self, media):
        item = self.ddlist.create_item(value=media, bg="#ddd")
        ui = MediaItemSchedule(item, parentTab=self, media=media)
        self._LS_SCHEDULE_UI.append(ui)
        ui.pack(padx=(4, 0), pady=(4, 0), expand=True)
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
        filtered = list(filter(lambda x: x["id"] == data["id"], ls))
        if len(filtered) > 0:
            self.saveEdit(ls, data)
        else:
            self.addMediaToList(data)
            self.addSchedule(data)
        self.f5(None)

    def f5(self, evt):
        super(SingleSchedule, self).f5(evt)
        ls = self.loadSchedule()
        self.totalDuration = reduce(lambda sum, x: sum + x["duration"], ls, 0)
        self.lblDura.config(
            text=f"total duration: {helper.convertSecNoToHMS(self.totalDuration)}"
        )

    def saveEdit(self, ls, media):
        newLs = list(map(lambda x: media if x["id"] == media["id"] else x, ls))
        self.clearData()
        self.writeSchedule(newLs)

    def calcRuntime(self, media):
        ls = self.loadSchedule()
        newLs = list(map(lambda x: media if x["id"] == media["id"] else x, ls))
        index = newLs.index(media)
        self.clearData()
        schedule = helper.calc_schedule_runtime(
            index, schedule=newLs, startTime=media["timepoint"]
        )
        self.writeSchedule(schedule)
        self.f5(None)

    def deleteMediaItem(self, lsId):
        self.rmvSchedule(lsId)

    def mergeAudioToSchedule(self, data):
        filtered = list(filter(lambda sch: sch.checked.get(), self._LS_SCHEDULE_UI))
        if len(filtered):
            if messagebox.askyesno(
                "PiepMe",
                "Are you sure merge this `audio` to all `selected schedule` items?",
            ):
                mapped = list(map(lambda sch: sch.id, filtered))
                self.updateScheduleAudioWithID(mapped, data or {})

    def updateScheduleAudioWithID(self, lsId, audio):
        def lambdaInjectAudio(sch):
            if sch["id"] in lsId:
                sch["audio"] = audio["url"] or ""
                sch["audio_name"] = audio["name"] or ""
            return sch

        #
        ls = self.loadSchedule()
        newLs = list(map(lambdaInjectAudio, ls))
        self.clearData()
        self.writeSchedule(newLs)
        self.f5(None)

    def stopAllAudio(self):
        for sch in self._LS_SCHEDULE_UI:
            if sch.playing_audio:
                sch.triggerStop()

