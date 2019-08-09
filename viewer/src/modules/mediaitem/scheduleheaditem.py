import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from src.utils import helper, scryto
from src.constants import UI
from src.modules.custom import ToolTip, PLabel
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from src.utils import store


class ScheduleHeadItem(tk.Frame):

    def __init__(self, parent, parentTab=None, media=None, *args, **kwargs):
        super(ScheduleHeadItem, self).__init__(parent, *args, **kwargs)
        self.parentTab = parentTab
        self.checked = tk.BooleanVar()
        self.id = ''
        self.name = ''
        self.path = ''
        self.actived = False
        self.isRunningSch = False
        self.set_data(media)
        self.initUI()
        #
        if self.isRunningSch:
            self.loadScheduleDE(None)

    def get_data(self):
        return {
            'path': self.path,
            'id': self.id,
            'name': self.name
        }

    def set_data(self, media):
        self.id = media['id'] if bool(media) else ''
        self.name = media['name'] if bool(media) else ''
        self.path = media['path'] if bool(media) else ''
        self.itemBg = '#F4ECF7'
        self.isRunningSch = self.id == 'STORE_SCHEDULE'

    def deleteSchedule(self, evt):
        if messagebox.askyesno("PiepMe", f"Are you sure to delete schedule: `{self.name}`?"):
            self.parentTab.rmvSchedule([self.id])
            self.destroy()
            self.parentTab.f5(None)

    def initUIEdit(self, edit=False):
        # var
        self.eName = tk.StringVar()
        #
        self.fEdit = tk.Frame(self, bg=self.itemBg)
        self.fEdit.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Name
        eName = self.eUrl = tk.Entry(self.fEdit, width=35 if edit else 20, textvariable=self.eName, borderwidth=5, relief=tk.FLAT)
        eName.insert(0, self.name if bool(self.name) else 'Name')
        eName.bind("<FocusIn>", lambda args: eName.select_range('0', tk.END))
        eName.pack(side=tk.LEFT, fill=tk.X, padx=5)
        # Add Date
        if not edit:
            self.packDate()
        # cancel
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}close-pink-s.png"))
        lblClose = tk.Label(self.fEdit, image=imageBin, cursor='hand2', bg=self.itemBg)
        lblClose.image = imageBin
        lblClose.bind("<Button-1>", self.cancelEditSchedule)
        ToolTip(lblClose, "Cancel")
        lblClose.pack(side=tk.RIGHT, padx=5)
        # save
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}check-green-s.png"))
        lblChk = tk.Label(self.fEdit, image=imageBin, cursor='hand2', bg=self.itemBg)
        lblChk.image = imageBin
        lblChk.bind("<Button-1>", self.saveEditSchedule)
        ToolTip(lblChk, "Save change")
        lblChk.pack(side=tk.RIGHT)
        #
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def initUI(self):
        self.fView = tk.Frame(self, bg=self.itemBg)
        self.fView.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        if not self.isRunningSch:
            # check all
            self.checkbox = tk.Checkbutton(self.fView, variable=self.checked, onvalue=True, offvalue=False, height=1, width=1, bd=0, relief=tk.FLAT, bg=self.itemBg)
            self.checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        self.lbl_name = PLabel(self.fView, text=self.name, justify=tk.LEFT, elipsis=25,
            font=UI.TITLE_FONT if self.isRunningSch else UI.TXT_FONT,
            fg='#ff2d55' if self.isRunningSch else "#000",
            cursor='hand2', bg=self.itemBg)
        self.lbl_name.bind('<Double-Button-1>', self.loadScheduleDE)
        self.lbl_name.pack(side=tk.LEFT, padx= 27 if self.isRunningSch else 0)
        ToolTip(self.lbl_name, self.name)
       
        if not self.isRunningSch:
            # bin
            imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b.png"))
            self.lbl_trash = tk.Label(self.fView, image=imageBin, cursor='hand2', bg=self.itemBg)
            self.lbl_trash.image = imageBin
            self.lbl_trash.bind("<Button-1>", self.deleteSchedule)
            self.lbl_trash.pack(side=tk.RIGHT)
            ToolTip(self.lbl_trash, "Delete")
            # edit
            imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}pen-b.png"))
            self.lblPen = tk.Label(self.fView, image=imageBin, cursor='hand2', bg=self.itemBg)
            self.lblPen.image = imageBin
            self.lblPen.bind("<Button-1>", self.editSchedule)
            self.lblPen.pack(side=tk.RIGHT)
            ToolTip(self.lblPen, "Edit")

        # push to schedule
        imgPush = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}push-right-b.png"))
        self.lblPush = tk.Label(self.fView, image=imgPush, cursor='hand2', bg=self.itemBg)
        self.lblPush.image = imgPush
        self.lblPush.bind("<Button-1>", self.loadScheduleDE)
        self.lblPush.pack(side=tk.RIGHT, padx=5, pady=5)
        #
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def loadScheduleDE(self, evt):
        self.parentTab.loadScheduleDE(self.get_data())
        self.changeBgFollowActivation(True)

    def changeBgFollowActivation(self, active=False):
        self.actived = active
        self.itemBg = '#E8DAEF' if self.actived else '#F4ECF7'
        self.fView.config(bg=self.itemBg)
        self.lbl_name.config(bg=self.itemBg)
        self.lblPush.config(bg=self.itemBg)
        #
        if not self.isRunningSch:
            self.checkbox.config(bg=self.itemBg)
            self.lbl_trash.config(bg=self.itemBg)
            self.lblPen.config(bg=self.itemBg)

    def editSchedule(self, evt):
        self.fView.pack_forget()
        self.initUIEdit(edit=True)

    def cancelEditSchedule(self, evt):
        if bool(self.id):
            self.fEdit.pack_forget()
            self.initUI()
        else:
            self.parentTab.f5(None)

    def saveEditSchedule(self, evt):
        self.parentTab.saveSchedule({
            'path': self.path,
            'id': self.id,
            'name': self.eName.get()
        })

class ScheduleHeadItemEdit(ScheduleHeadItem):
    def __init__(self, parent, parentTab=None, media=None, *args, **kwargs):
        super(ScheduleHeadItemEdit, self).__init__(parent, parentTab=parentTab, media=media, *args, **kwargs)

    def initUI(self):
        self.initUIEdit()

    def saveEditSchedule(self, evt):
        if not bool(self.id):# create
            self.id = scryto.hash_md5_with_time(self.path)
            date = self.calendar.get()
            self.path = date.replace('/', '')

        super(ScheduleHeadItemEdit, self).saveEditSchedule(evt)
        
    def packDate(self):
        schDate = self.parentTab.findLastDateInSchedule()
        #
        self.calendar = DateEntry(self.fEdit, width=10, background='#D2B4DE', foreground='#000', borderwidth=2, selectbackground='#E8DAEF',
                                day=schDate.day, month=schDate.month, year=schDate.year, firstweekday='sunday', locale='vi_VN')
        self.calendar.pack(side=tk.LEFT, fill=tk.X, padx=(5, 0))
        schName = self.parentTab.generateNameFromDate(schDate)
        self.eName.set(schName)
        self.calendar.bind('<<DateEntrySelected>>', self.selectedDateEntry)

    def selectedDateEntry(self, evt):
        schName = self.parentTab.generateNameFromDate(self.calendar.get_date())
        self.eName.set(schName)

