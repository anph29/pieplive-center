import vlc
import tkinter as tk
from src.modules.custom import PLabel
from PIL import Image, ImageTk
from src.utils import helper
from src.constants import UI
from .mediaitem import MediaItem
from src.enums import MediaType
from src.modules.custom import ToolTip

class MediaItemDnD(MediaItem):

    def __init__(self, parent, parentTab=None, media=None, *args, **kwargs):
        super(MediaItemDnD, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parentTab = parentTab
        self.set_data(media)
        self.initGUI()

    def initGUI(self):
        #
        wrapper = tk.Frame(self)
        wrapper.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # push to schedule
        imgPush = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}push-left-b.png"))
        lblPush = tk.Label(wrapper, image=imgPush, cursor='hand2')
        lblPush.image = imgPush
        lblPush.bind("<Button-1>", self.callParentAddSchedule)
        lblPush.pack(side=tk.LEFT, padx=5, pady=5)
        #
        checkbox = tk.Checkbutton(wrapper, variable=self.checked, onvalue=True, offvalue=False, height=1, width=1, bd=0, relief=tk.FLAT)
        checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        lbl_name = PLabel(wrapper, text=self.name, justify=tk.LEFT, elipsis=40, font=UI.TXT_FONT, fg="#000", cursor='hand2')
        lbl_name.pack(side=tk.LEFT)
        # bin
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b.png"))
        lbl_trash = tk.Label(wrapper, image=imageBin, cursor='hand2')
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deletemedia)
        ToolTip(lbl_trash, "Delete")
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #duration
        if self.parentTab.tabType == MediaType.VIDEO:
            hms = helper.convertSecNoToHMS(self.duration)
            dura = PLabel(wrapper, text=hms, fg='#ff2d55', font=UI.TXT_FONT)
            dura.pack(side=tk.RIGHT, padx=10)

    def deletemedia(self, evt):
        super(MediaItemDnD, self).deletemedia(evt)
        self.parentTab.tabRefresh(None)

    def callParentAddSchedule(self, evt):
        self.parentTab.callShowPopup(self.get_data())