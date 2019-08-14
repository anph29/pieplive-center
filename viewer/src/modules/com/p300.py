import tkinter as tk


class P300(tk.Frame):
    def __init__(self, parent, p300=None, *args, **kwargs):
        super(P300, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.set_data(p300)
        self.initGUI()

    def get_data(self):
        return {
            "PV325": self.PV325,
            "PP300": self.PP300,
            "FO100": self.FO100,
            "FT300": self.FT300,
            "PO323": self.PO323,
        }

    def set_data(self, p300):
        self.PV325 = p300["PV325"] or ""
        self.PP300 = p300["PP300"] or 0
        self.PV301 = p300["PV301"] or ""
        self.FO100 = p300["FO100"] or 0
        self.FT300 = p300["FT300"] or 0
        self.PO322 = p300["PO322"] or {}
        self.PO323 = p300["PO323"] or {}

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
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}trash-b.png"))
        lbl_trash = tk.Label(wrapper, image=imageBin, cursor="hand2", bg=self.itemBg)
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deleteMedia)
        ToolTip(lbl_trash, "Delete")
        lbl_trash.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # edit
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}pen-b.png"))
        lblPen = tk.Label(wrapper, image=imageBin, cursor="hand2", bg=self.itemBg)
        lblPen.image = imageBin
        lblPen.bind("<Button-1>", self.editMedia)
        ToolTip(lblPen, "Edit")
        lblPen.pack(side=tk.RIGHT)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # push to schedule
        imgPush = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}add-to-sch.png"))
        lblPush = tk.Label(wrapper, image=imgPush, cursor="hand2", bg=self.itemBg)
        lblPush.image = imgPush
        lblPush.bind("<Button-1>", self.callParentAddSchedule)
        lblPush.pack(side=tk.RIGHT, padx=5, pady=5)
        # traffic lignt
        if self.parentTab.tabType == MediaType.PRESENTER:
            frame = tk.PhotoImage(file=f"{helper._ICONS_PATH}live-red.png")
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
        self.parentTab.callShowPopup(self.get_data())
