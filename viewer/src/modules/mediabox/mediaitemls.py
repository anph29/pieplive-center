import vlc
import tkinter as tk
from tkinter import ttk, messagebox
from src.modules.custom import PLabel
from PIL import Image, ImageTk
from src.utils import helper, scryto
from src.constants import UI

class MediaItemLs(tk.Frame):

    def __init__(self, parent, parentTab=None, media=None, *args, **kwargs):
        super(MediaItemLs, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parentTab = parentTab
        self.set_data(media)
        self.after(100, self.initGUI)

    def get_data(self):
        return {
            'id':self.id,
            'name': self.name, 
            'url': self.url, 
            'type': self.mtype
        }

    def set_data(self, media):
        self.id = media['id']
        self.name = media['name']
        self.url = media['url']
        self.mtype = media['type']

    def initGUI(self):
        self.wrapper = tk.Frame(self, relief=tk.FLAT, bd=1 ,bg="#BDC3C7")
        self.checked = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self.wrapper, variable=self.checked, onvalue=True, offvalue=False, height=1, width=1, bd=0, relief=tk.FLAT)
        self.checkbox.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        # label
        lbl_name = PLabel(self.wrapper, text=self.name, justify=tk.LEFT, elipsis=25, font=UI.TXT_FONT, fg="#000")
        lbl_name.pack(side=tk.LEFT)
        # bin
        imageBin = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}/trash-b.png"))
        lbl_trash = tk.Label(self.wrapper, image=imageBin, cursor='hand2')
        lbl_trash.image = imageBin
        lbl_trash.bind("<Button-1>", self.deletemedia)
        lbl_trash.pack(side=tk.RIGHT)
        self.wrapper.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def deletemedia(self, evt):
        if messagebox.askyesno("PiepMe", "Are you sure to delete this resource?"):
            self.parentTab.deleteMediaItem([self.id])
            self.destroy()

    