import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from src.utils import helper
from src.constants import UI
from src.modules.custom import ToolTip, PLabel

class ScheduleHeadItem(tk.Frame):

    def __init__(self, parent, parentTab=None, media=None, *args, **kwargs):
        super(ScheduleHeadItem, self).__init__(parent, *args, **kwargs)
        self.parentTab = parentTab
        self.checked = tk.BooleanVar()
        self.id = ''
        self.name = ''
        self.path = ''
        self.set_data(media)

    def get_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path
        }

    def set_data(self, media):
        self.id = media['id']
        self.name = media['name']
        self.path = media['path']

    def deleteSchedule(self, evt):
        if messagebox.askyesno("PiepMe", "Are you sure to delete this schedule?"):
            self.parentTab.deleteScheduleItem([self.id])
            self.destroy()
            self.parentTab.tabRefresh(None)

    def initGUI(self):
        #
        wrapper = tk.Frame(self)
        wrapper.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # check all
        checkbox = tk.Checkbutton(wrapper, variable=self.checked, onvalue=True, offvalue=False, height=1, width=1, bd=0, relief=tk.FLAT)
        checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        lbl_name = PLabel(wrapper, text=self.name, justify=tk.LEFT, elipsis=35, font=UI.TXT_FONT, fg="#000", cursor='hand2')
        ToolTip(lbl_name, self.name)
        lbl_name.pack(side=tk.LEFT)
        # bin
        imageBin = ImageTk.PhotoImage(
            Image.open(f"{helper._ICONS_PATH}trash-b.png"))
        lbl_trash = tk.Label(wrapper, image=imageBin, cursor='hand2')
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deleteSchedule)
        ToolTip(lbl_trash, "Delete")
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # edit
        imageBin = ImageTk.PhotoImage(
            Image.open(f"{helper._ICONS_PATH}pen-b.png"))
        lblPen = tk.Label(wrapper, image=imageBin, cursor='hand2')
        lblPen.image = imageBin
        lblPen.bind("<Button-1>", self.editSchedule)
        ToolTip(lblPen, "Edit")
        lblPen.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def editSchedule(self, evt):
        pass