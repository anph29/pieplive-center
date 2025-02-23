import tkinter as tk
from src.modules.custom import PLabel
import PIL
from PIL import Image, ImageTk
from src.utils import helper
from src.constants import UI
from .mediaitem import MediaItem
from src.enums import MediaType
from src.modules.custom import ToolTip, CanvasC


class MediaItemDnD(MediaItem):
    def __init__(self, parent, parentTab=None, media=None, *args, **kwargs):
        super(MediaItemDnD, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parentTab = parentTab
        self.set_data(media)
        self.initGUI()

    def set_data(self, media):
        super(MediaItemDnD, self).set_data(media)
        self.itemBg = "#F2F2F2"
        self.audioSrc = self.url

    def initGUI(self):
        #
        wrapper = tk.Frame(self, bg=self.itemBg)
        wrapper.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # checkbox
        checkbox = tk.Checkbutton(
            wrapper,
            variable=self.checked,
            onvalue=True,
            offvalue=False,
            height=1,
            width=1,
            bd=0,
            relief=tk.FLAT,
            bg=self.itemBg,
        )
        checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        lbl_name = PLabel(
            wrapper,
            text=self.name,
            justify=tk.LEFT,
            elipsis=(35, 30)[self.parentTab.tabType == MediaType.VIDEO],
            font=UI.TXT_FONT,
            fg="#000",
            cursor="hand2",
            bg=self.itemBg,
        )
        lbl_name.pack(side=tk.LEFT)
        lbl_name.bind("<Double-Button-1>", self.callParentAddSchedule)
        ToolTip(lbl_name, self.name)
        # bin
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICON_PATH}trash-b.png"))
        lbl_trash = tk.Label(wrapper, image=imageBin, cursor="hand2", bg=self.itemBg)
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deleteMedia)
        ToolTip(lbl_trash, "Delete")
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # edit
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICON_PATH}pen-b.png"))
        lblPen = tk.Label(wrapper, image=imageBin, cursor="hand2", bg=self.itemBg)
        lblPen.image = imageBin
        lblPen.bind("<Button-1>", self.editMedia)
        ToolTip(lblPen, "Edit")
        lblPen.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # push to schedule
        imgPush = ImageTk.PhotoImage(
            Image.open(
                f"{helper._ICON_PATH}{'ic_audio' if self.parentTab.tabType == MediaType.AUDIO else 'add-to-sch'}.png"
            )
        )
        lblPush = tk.Label(wrapper, image=imgPush, cursor="hand2", bg=self.itemBg)
        lblPush.image = imgPush
        lblPush.bind(
            "<Button-1>",
            self.mergeAudio
            if self.parentTab.tabType == MediaType.AUDIO
            else self.callParentAddSchedule,
        )
        lblPush.pack(side=tk.RIGHT, padx=5, pady=5)
        # play
        if self.parentTab.tabType == MediaType.AUDIO:
            imagePlay = ImageTk.PhotoImage(
                Image.open(f"{helper._ICON_PATH}play-mp3-b.png")
            )
            self.lblPlay = tk.Label(
                wrapper, image=imagePlay, bg=self.itemBg, cursor="hand2"
            )
            self.lblPlay.image = imagePlay
            self.lblPlay.bind("<Button-1>", self.playAudio)
            self.lblPlay.pack(side=tk.RIGHT)
        # traffic light
        if self.parentTab.tabType == MediaType.PRESENTER:
            frame = tk.PhotoImage(file=f"{helper._ICON_PATH}live-red.png")
            self.light = tk.Label(
                wrapper, width=16, height=16, image=frame, bg=self.itemBg
            )
            self.light.photo = frame
            self.light.pack(side=tk.RIGHT)
        # duration
        if self.parentTab.tabType == MediaType.VIDEO:
            hms = helper.convertSecNoToHMS(self.duration)
            dura = PLabel(
                wrapper, text=hms, fg="#008000", font=UI.TXT_FONT, bg=self.itemBg
            )
            dura.pack(side=tk.RIGHT, padx=10)

    def editMedia(self, evt):
        self.parentTab.showEditMedia(self.get_data())

    def deleteMedia(self, evt):
        super(MediaItemDnD, self).deleteMedia(evt)
        self.parentTab.f5(None)

    def callParentAddSchedule(self, evt):
        self.parentTab.showPopupAddSchedule(self.get_data())

    def mergeAudio(self, evt):
        self.parentTab.mergeAudioToSchedule(self.get_data())

    