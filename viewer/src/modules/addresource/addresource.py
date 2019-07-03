
from src.utils import ftype, helper
import tkinter as tk
from tkinter import filedialog
from src.utils import tk_helper

class AddResource(object):
    use_local = False
    addCamPopup = None
    error = False

    def __init__(self, parent):
        self.parent = parent

    def initGUI(self, evt):
        # first destroy
        if None is not self.addCamPopup:
            self.addCamPopup.destroy()
        # init
        self.addCamPopup = tk_helper.makePiepMePopup(
            'Add Media', w=400, h=200)
        # var
        self.name = tk.StringVar()
        self.url = tk.StringVar()
        # name
        f_name = tk.Frame(self.addCamPopup, pady=10)
        l_name = tk.Label(f_name, text="Name:", width=6, anchor=tk.W)
        l_name.pack(side=tk.LEFT, fill=tk.Y)
        self.e_name = tk.Entry(f_name, textvariable=self.name, width=100, borderwidth=5, relief=tk.FLAT)
        self.e_name.pack(side=tk.LEFT, fill=tk.X)
        f_name.pack(side=tk.TOP, fill=tk.X)
        # URL
        f_url = tk.Frame(self.addCamPopup,  pady=10)
        l_url = tk.Label(f_url, text="URL:", width=6, anchor=tk.W)
        l_url.pack(side=tk.LEFT, fill=tk.Y)
        self.e_url = tk.Entry(f_url, textvariable=self.url, width=36, borderwidth=5, relief=tk.FLAT)
        self.e_url.pack(side=tk.LEFT, fill=tk.X)
        btn_choose = tk.Button( f_url, text="Choose..", relief=tk.RAISED, padx=5, pady=5, command=self.askFileName)
        btn_choose.configure(width=7)
        btn_choose.pack(side=tk.RIGHT, fill=tk.Y)
        f_url.pack(side=tk.TOP, fill=tk.X)
        # error msg
        self.f_error = tk.Frame(self.addCamPopup)
        l_error = tk.Label(self.f_error, text="File not allowed!", fg="#f00")
        l_error.pack(side=tk.LEFT, fill=tk.Y)
        # bot button
        f_btn = tk.Frame(self.addCamPopup, pady=10)
        btn_cancel = tk.Button(f_btn, text="Cancel", bd=2, relief=tk.RAISED, command=self.addCamPopup.destroy)
        btn_cancel.configure(width=7)
        btn_cancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btn_ok = tk.Button(f_btn, text="OK", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.on_ok)
        btn_ok.configure(width=7)
        btn_ok.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        f_btn.pack(side=tk.BOTTOM, fill=tk.X)

    def askFileName(self):
        self.f_error.pack_forget()
        fname = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("video files", "*.mov *.mp4"), ("image files", "*.png *.jpg"), ("all files", "*.*")))
        if ftype.isImage(fname):
            self.local_file(fname, 'IMG')
        elif ftype.isVideo(fname):
            self.local_file(fname, 'VIDEO')
        else:
            self.f_error.pack(side=tk.TOP, fill=tk.X)

        self.e_url.delete(0, tk.END)
        self.e_url.insert(0, fname)

    def add_to_lscam(self):
        dt = {
            "name": str(self.name.get()),
            "url": str(self.url.get()),
            "type": self.mtype
        }
        helper._add_to_lscam(dt)
        self.parent.addToTabCamera(dt)
        self.addCamPopup.destroy()

    def on_ok(self):
        if self.use_local:
            self.add_to_lscam()
        elif len(self.name.get()) > 0:
            self.mtype = self.validateResouce()
            if self.mtype:
                self.add_to_lscam()
            else:
                self.f_error.pack(side=tk.TOP, fill=tk.X)
        else:
            self.f_error.pack(side=tk.TOP, fill=tk.X)

    def local_file(self, fpath, ftype):
        self.use_local = True
        self.mtype = ftype

    def validateResouce(self):
        URL = str(self.url.get()).upper()
        if 'RTSP' in URL:
            return 'RTSP'
        elif 'MP4' in URL:
            return 'MP4'
        elif 'M3U8' in URL:
            return 'M3U8'
        else:
            return False
