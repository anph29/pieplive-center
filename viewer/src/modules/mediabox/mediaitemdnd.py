import vlc
import tkinter as tk
from tkinter import ttk, messagebox
from src.modules.custom import PLabel
from PIL import Image, ImageTk
from src.utils import helper, scryto
from src.constants import UI
from .mediaitem import MediaItem

class MediaItemDnD(MediaItem):

    def __init__(self, parent, parentTab=None, media=None, *args, **kwargs):
        super(MediaItemDnD, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parentTab = parentTab
        self.set_data(media)
        self.initGUI()


    def initGUI(self):
        self.checkbox = tk.Checkbutton(self, variable=self.checked, onvalue=True, offvalue=False, height=1, width=1, bd=0, relief=tk.FLAT)
        self.checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        lbl_name = PLabel(self, text=self.name, justify=tk.LEFT, elipsis=40, font=UI.TXT_FONT, fg="#000")
        lbl_name.pack(side=tk.LEFT)
        # bin
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}/trash-b.png"))
        lbl_trash = tk.Label(self, image=imageBin, cursor='hand2')
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deletemedia)
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def deletemedia(self, evt):
         super(MediaItemDnD, self).deletemedia(evt)
        #  self.delete_item()