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
        self.initUI()

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
        if messagebox.askyesno("PiepMe", f"Are you sure to delete schedule: `{self.name}`?"):
            self.parentTab.deleteScheduleItem([self.id])
            self.destroy()
            self.parentTab.f5(None)

    def initUI(self):
        wrapper = tk.Frame(self)
        wrapper.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # check all
        checkbox = tk.Checkbutton(wrapper, variable=self.checked, onvalue=True, offvalue=False, height=1, width=1, bd=0, relief=tk.FLAT)
        checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        lbl_name = PLabel(wrapper, text=self.name, justify=tk.LEFT, elipsis=35, font=UI.TXT_FONT, fg="#000", cursor='hand2')
        ToolTip(lbl_name, self.name)
        lbl_name.pack(side=tk.LEFT)
        # push to schedule
        imgPush = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}push-right-b.png"))
        lblPush = tk.Label(wrapper, image=imgPush, cursor='hand2')
        lblPush.image = imgPush
        lblPush.bind("<Button-1>", self.loadScheduleDE)
        lblPush.pack(side=tk.RIGHT, padx=5, pady=5)
        # bin
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b.png"))
        lbl_trash = tk.Label(wrapper, image=imageBin, cursor='hand2')
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deleteSchedule)
        ToolTip(lbl_trash, "Delete")
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # edit
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}pen-b.png"))
        lblPen = tk.Label(wrapper, image=imageBin, cursor='hand2')
        lblPen.image = imageBin
        lblPen.bind("<Button-1>", self.editSchedule)
        ToolTip(lblPen, "Edit")
        lblPen.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def initUIEdit(self):
        # var
        self.eName = tk.StringVar()
        #
        wrapper = tk.Frame(self)
        wrapper.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # check all
        checkbox = tk.Checkbutton(wrapper, variable=self.checked, onvalue=True, offvalue=False, height=1, width=1, bd=0, relief=tk.FLAT)
        checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        eName = self.eUrl = tk.Entry(wrapper, textvariable=self.eName, width=45, borderwidth=5, relief=tk.FLAT)
        eName.pack(side=tk.LEFT)
        # push to schedule
        imgPush = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}push-right-b.png"))
        lblPush = tk.Label(wrapper, image=imgPush, cursor='hand2')
        lblPush.image = imgPush
        lblPush.bind("<Button-1>", self.loadScheduleDE)
        lblPush.pack(side=tk.RIGHT, padx=5, pady=5)
        # cancel
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}close-pink.png"))
        lbl_trash = tk.Label(wrapper, image=imageBin, cursor='hand2')
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.cancelEditSchedule)
        ToolTip(lbl_trash, "Cancel")
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # save
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}green-check.png"))
        lblPen = tk.Label(wrapper, image=imageBin, cursor='hand2')
        lblPen.image = imageBin
        lblPen.bind("<Button-1>", self.saveEditSchedule)
        ToolTip(lblPen, "Save change")
        lblPen.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def loadScheduleDE(self, evt):
        self.parentTab.loadScheduleDE(self.get_data())

    def editSchedule(self, evt):
        self.parentTab.editSchedule(self.get_data())

    def cancelEditSchedule(self):
        pass

    def saveEditSchedule(self):
        pass