import tkinter as tk
from src.modules.custom import PLabel
import PIL
from PIL import Image, ImageTk
from src.utils import helper
from src.constants import UI
from .mediaitem import MediaItem
from src.modules.custom import ToolTip


class MediaItemSchedule(MediaItem):
    def __init__(self, parent, media=None, parentTab=None, *args, **kwargs):
        if "elipsis" in kwargs:
            self.nameElipsis = kwargs["elipsis"]
            del kwargs["elipsis"]
        else:
            self.nameElipsis = 60
        super(MediaItemSchedule, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parentTab = parentTab
        self.set_data(media)
        self.initGUI()

    def get_data(self):
        data = super(MediaItemSchedule, self).get_data()
        data["duration"] = self.duration
        data["timepoint"] = self.timepoint
        return data

    def set_data(self, media):
        super(MediaItemSchedule, self).set_data(media)
        self.duration = int(media["duration"]) if "duration" in media else 0
        self.timepoint = int(media["timepoint"]) if "timepoint" in media else 0
        self.itemBg = "#E8F6F3"
        self.audioSrc = self.audio

    def initGUI(self):
        #
        self.wrapper = tk.Frame(self, bd=10, relief=tk.FLAT, height=30, bg=self.itemBg)
        self.wrapper.pack(side=tk.BOTTOM, fill=tk.X)
        # chkbx
        self.checkbox = tk.Checkbutton(
            self.wrapper,
            variable=self.checked,
            onvalue=True,
            offvalue=False,
            height=1,
            width=1,
            bd=0,
            relief=tk.FLAT,
            bg=self.itemBg,
        )
        self.checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        lbl_name = PLabel(
            self.wrapper,
            text=self.name,
            justify=tk.LEFT,
            elipsis=self.nameElipsis,
            font=UI.TXT_FONT,
            fg="#000",
            bg=self.itemBg,
        )
        ToolTip(lbl_name, self.name)
        lbl_name.pack(side=tk.LEFT)
        # bin
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICON_PATH}trash-b.png"))
        lbl_trash = tk.Label(
            self.wrapper, image=imageBin, cursor="hand2", bg=self.itemBg
        )
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deleteMedia)
        ToolTip(lbl_trash, "Delete")
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # edit
        imPen = ImageTk.PhotoImage(Image.open(f"{helper._ICON_PATH}pen-b.png"))
        lblPen = tk.Label(self.wrapper, image=imPen, cursor="hand2", bg=self.itemBg)
        lblPen.image = imPen
        lblPen.bind("<Button-1>", self.editMedia)
        ToolTip(lblPen, "Edit")
        lblPen.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # audio
        if bool(self.audio):
            # play
            imagePlay = ImageTk.PhotoImage(
                Image.open(f"{helper._ICON_PATH}play-mp3-b.png")
            )
            self.lblPlay = tk.Label(
                self.wrapper, image=imagePlay, bg=self.itemBg, cursor="hand2"
            )
            self.lblPlay.image = imagePlay
            self.lblPlay.bind("<Button-1>", self.playAudio)
            self.lblPlay.pack(side=tk.RIGHT)
            ToolTip(self.lblPlay, self.audio_name)
        # duration
        hms = helper.convertSecNoToHMS(self.duration)
        dura = PLabel(
            self.wrapper,
            text=f"duration: {hms}",
            fg="#008000",
            font=UI.TXT_FONT,
            bg=self.itemBg,
        )
        dura.pack(side=tk.RIGHT, padx=(5, 5 if bool(self.audio) else 30))
        # timepoint
        HMS = helper.convertSecNoToHMS(self.timepoint)
        runtime = PLabel(
            self.wrapper,
            text=f"runtime: {HMS}",
            fg="#00F",
            font=UI.TXT_FONT,
            cursor="hand2",
            bg=self.itemBg,
        )
        runtime.bind("<Button-1>", self.editRuntime)
        runtime.pack(side=tk.RIGHT, padx=5)

    def editMedia(self, evt):
        if self.parentTab.notWarningLocked():
            self.parentTab.showAddToSchedulePopup(self.get_data(), edit=True)

    def editRuntime(self, evt):
        if self.parentTab.notWarningLocked():
            self.parentTab.editRuntime(self.get_data())

    def deleteMedia(self, evt):
        super(MediaItemSchedule, self).deleteMedia(evt)
        self.parentTab.f5(None)
