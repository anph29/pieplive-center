import os
from src.utils import ftype, helper
import tkinter as tk
from tkinter import filedialog, ttk
from src.utils import tk_helper, scryto
from src.constants import UI
from src.enums import TabType

class AddResource(object):
    useLocal = False
    addCamPopup = None
    error = False

    def __init__(self, parent):
        self.parent = parent

    def initGUI(self, evt):
        # first destroy
        if None is not self.addCamPopup:
            self.addCamPopup.destroy()
        self.addCamPopup = tk_helper.makePiepMePopup('Add Media', w=400, h=250, padx=0, pady=0)
        self.makeMasterTab()
    
    def makeMasterTab(self):
        #
        self.masterTab = ttk.Notebook(self.addCamPopup)
        self.masterTab.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(2,0))
        # 1
        self.tabFile = self.initTabFileUI()
        self.masterTab.add(self.tabFile, text="Choose file")
        # 2
        self.tabFolder = self.initTabFolderUI()
        self.masterTab.add(self.tabFolder, text="Choose folder")
        #
        self.masterTab.select(self.tabFolder)
        self.masterTab.enable_traversal()

    def initTabFolderUI(self):
        fFolder = tk.Frame(self.addCamPopup)
        # URL
        fUrl = tk.Frame(fFolder, pady=10, padx=20)
        lUrl = tk.Label(fUrl, text="URL:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lUrl.pack(side=tk.LEFT, fill=tk.Y)
        self.eUrlFolder = tk.Entry(fUrl, textvariable=self.url, width=36, borderwidth=5, relief=tk.FLAT)
        self.eUrlFolder.pack(side=tk.LEFT, fill=tk.X)
        btnChoose = tk.Button(fUrl, text="Choose..", relief=tk.RAISED, padx=5, pady=5, command=self.askFolderName, font=UI.TXT_FONT)
        btnChoose.configure(width=7)
        btnChoose.pack(side=tk.RIGHT, fill=tk.Y)
        fUrl.pack(side=tk.TOP, fill=tk.X)
        # bot button
        fBtn = tk.Frame(fFolder,  pady=10, padx=20)
        btnCancel = tk.Button(fBtn, text="Cancel", bd=2, relief=tk.RAISED, command=self.addCamPopup.destroy)
        btnCancel.configure(width=7)
        btnCancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btnOk = tk.Button(fBtn, text="OK", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.onOkFolder)
        btnOk.configure(width=7)
        btnOk.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        fBtn.pack(side=tk.BOTTOM, fill=tk.X)
        return fFolder

    def initTabFileUI(self):
        fFile = tk.Frame(self.addCamPopup)
        # var
        self.name = tk.StringVar()
        self.url = tk.StringVar()
        # name
        fName = tk.Frame(fFile, pady=10, padx=20)
        lName = tk.Label(fName, text="Name:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lName.pack(side=tk.LEFT, fill=tk.Y)
        self.eName = tk.Entry(fName, textvariable=self.name, width=100, borderwidth=5, relief=tk.FLAT)
        self.eName.pack(side=tk.LEFT, fill=tk.X)
        fName.pack(side=tk.TOP, fill=tk.X)
        # URL
        fUrl = tk.Frame(fFile, pady=10, padx=20)
        lUrl = tk.Label(fUrl, text="URL:", width=6, anchor=tk.W, font=UI.TXT_FONT)
        lUrl.pack(side=tk.LEFT, fill=tk.Y)
        self.eUrl = tk.Entry(fUrl, textvariable=self.url, width=36, borderwidth=5, relief=tk.FLAT)
        self.eUrl.pack(side=tk.LEFT, fill=tk.X)
        btnChoose = tk.Button(fUrl, text="Choose..", relief=tk.RAISED, padx=5, pady=5, command=self.askFileName, font=UI.TXT_FONT)
        btnChoose.configure(width=7)
        btnChoose.pack(side=tk.RIGHT, fill=tk.Y)
        fUrl.pack(side=tk.TOP, fill=tk.X)
        # error msg
        self.fError = tk.Frame(fFile)
        lError = tk.Label(self.fError, text="File not allowed!", fg="#f00")
        lError.pack(side=tk.LEFT, fill=tk.Y)
        # bot button
        fBtn = tk.Frame(fFile, pady=10, padx=20)
        btnCancel = tk.Button(fBtn, text="Cancel", bd=2, relief=tk.RAISED, command=self.addCamPopup.destroy)
        btnCancel.configure(width=7)
        btnCancel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        btnOk = tk.Button(fBtn, text="OK", bd=2, bg="#ff2d55", fg="#fff", relief=tk.RAISED, command=self.onOkFile)
        btnOk.configure(width=7)
        btnOk.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        fBtn.pack(side=tk.BOTTOM, fill=tk.X)

        return fFile

    def getTypeAllowedFromTabType(self):
        ''''''
        if self.parent.tabType == TabType.IMAGE:
            return (("image files", "*.png *.jpg"),("all files", "*.*"))
        elif self.parent.tabType == TabType.VIDEO:
            return (("video files", "*.mov *.mp4"),("all files", "*.*"))

    def askFileName(self):
        self.fError.pack_forget()
        path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=self.getTypeAllowedFromTabType())
        fname = os.fsdecode(path)
        if ftype.isImage(fname):
            self.useLocal = True
            self.mtype = 'IMG'
        elif ftype.isVideo(fname):
            self.useLocal = True
            self.mtype = 'VIDEO'
        else:
            self.fError.pack(side=tk.TOP, fill=tk.X)
        # fill data
        self.eName.delete(0, tk.END)
        self.eName.insert(0, (fname.split('/')[-1]).split('.')[0])
        self.eUrl.delete(0, tk.END)
        self.eUrl.insert(0, fname)

    def localFile(self, ftype):
        self.useLocal = True
        self.mtype = ftype

    def askFolderName(self):
        self.directory = filedialog.askdirectory()
        self.eUrlFolder.delete(0, tk.END)
        self.eUrlFolder.insert(0, self.directory)


    def onOkFolder(self):
        for file in os.listdir(self.directory):
            fname = os.fsdecode(file)
            fpath = os.path.join(self.directory, fname).replace('\\', '/')
            if os.path.isfile(fpath):
                isImg = ftype.isImage(fpath)
                isVideo = ftype.isVideo(fpath)
                if isImg or isVideo:
                    dt = {
                        "id" : scryto.hash_md5_with_time(fpath),
                        "name": (fpath.split('/')[-1]).split('.')[0],
                        "url": fpath
                    }
                    if self.parent.tabType == TabType.IMAGE and isImg:
                        dt["type"] = 'IMG'
                        self.parent.addMediaBoxToList(dt)
                        self.parent.addMedia(dt)
                    elif self.parent.tabType == TabType.VIDEO and isVideo:
                        dt["type"] = 'VIDEO'
                        self.parent.addMediaBoxToList(dt)
                        self.parent.addMedia(dt)
        #   
        self.addCamPopup.destroy()


    def onOkFile(self):
        if self.useLocal:
            self.addSingleToLsMedia()
        elif len(self.name.get()) > 0:
            self.mtype = helper.getMTypeFromUrl(self.url.get())
            if self.mtype:
                self.addSingleToLsMedia()
            else:
                self.fError.pack(side=tk.TOP, fill=tk.X)
        else:
            self.fError.pack(side=tk.TOP, fill=tk.X)

    def addSingleToLsMedia(self):
        url = self.url.get()
        dt = {
            "name": str(self.name.get()),
            "url": str(url),
            "type": self.mtype,
            "id" : scryto.hash_md5_with_time(url)
        }
        self.parent.addMediaBoxToList(dt)
        self.parent.addMedia(dt)
        self.addCamPopup.destroy()
