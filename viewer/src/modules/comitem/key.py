import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from src.modules.custom import ToolTip
from src.utils import helper
from src.modules.custom import PLabel
from src.constants import UI


class Key(tk.Frame):
    def __init__(self, parent, parentTab=None, key=None, *args, **kwargs):
        super(Key, self).__init__(parent, *args, **kwargs)
        self.parentTab = parentTab
        self.checked = tk.BooleanVar()
        self.id = ""
        self.name = ""
        self.path = ""
        self.actived = False
        self.isRunningSch = False
        self.itemBg = "#F2F2F2"
        self.set_data(key)
        self.initUI()

    def get_data(self):
        return {
            "id": self.id,
            "label": self.label,
            "key_a": self.key_a,
            "key_b": self.key_b,
            "PLAY": self.PLAY,
            "P300": self.P300,
        }

    def set_data(self, key):
        self.id = key["id"]
        self.label = key["label"]
        self.key_a = key["key_a"]
        self.key_b = key["key_b"]
        self.PLAY = key["PLAY"]
        self.P300 = key["P300"]

    def deleteKey(self, evt):
        if messagebox.askyesno(
            "PiepMe", f"Are you sure to delete key: `{self.label}`?"
        ):
            self.parentTab.rmvKey([self.id])
            self.destroy()
            self.parentTab.f5(None)

    def initUI(self):
        self.fView = tk.Frame(self, bg=self.itemBg)
        self.fView.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # check all
        self.checkbox = tk.Checkbutton(
            self.fView,
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
        self.lbl_name = PLabel(
            self.fView,
            text=self.label,
            justify=tk.LEFT,
            elipsis=35,
            font=UI.TITLE_FONT if self.isRunningSch else UI.TXT_FONT,
            fg="#ff2d55" if self.isRunningSch else "#000",
            cursor="hand2",
            bg=self.itemBg,
        )
        self.lbl_name.pack(side=tk.LEFT)
        ToolTip(self.lbl_name, self.name)

        # bin
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b.png"))
        self.lbl_trash = tk.Label(
            self.fView, image=imageBin, cursor="hand2", bg=self.itemBg
        )
        self.lbl_trash.image = imageBin
        self.lbl_trash.bind("<Button-1>", self.deleteKey)
        self.lbl_trash.pack(side=tk.RIGHT)
        ToolTip(self.lbl_trash, "Delete")
        # edit
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}pen-b.png"))
        lblPen = tk.Label(self.fView, image=imageBin, cursor="hand2", bg=self.itemBg)
        lblPen.image = imageBin
        lblPen.bind("<Button-1>", self.editKey)
        ToolTip(lblPen, "Edit")
        lblPen.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def editKey(self, evt):
        self.parentTab.showEditKey(self.get_data())

