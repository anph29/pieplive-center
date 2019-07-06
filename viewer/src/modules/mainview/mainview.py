import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import helper, store
from src.modules.mediatab import MediaTab, TabType
from src.models import Q170_model, L500_model
from src.enums import Q180
from src.constants import WS, UI
from src.modules.custom import LabeledCombobox
from PIL import Image, ImageTk
from src.modules.menu import MainMenu
from uuid import getnode as get_mac


class MainView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MainView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.after(100, self.initGUI)

    def setStyle(self):
        """"""
        style = ttk.Style()
        style.theme_create("TabStyle", parent="alt", settings={
            "TNotebook": {
                "configure": {"tabmargins": [5, 0, 0, 5]}  # L T R B
            },
            "TNotebook.Tab": {
                "configure": {"padding": [15, 5, 15, 5]}
            }
        })
        style.theme_use("TabStyle")

    def initGUI(self):
        """"""
        self.setStyle()
        #
        self.updateMenu()
        #
        self.showToolbar()
        #
        self.showMasterTab()
        
    def showMasterTab(self):
        self.masterTab = ttk.Notebook(self)
        self.masterTab.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # 1
        self.tab_image = self.initTabContent(TabType.IMAGE)
        self.masterTab.add(self.tab_image, text="Images")
        # 2
        self.tab_video = self.initTabContent(TabType.VIDEO)
        self.masterTab.add(self.tab_video, text="Videos")
        # 3
        self.tab_camera = self.initTabContent(TabType.CAMERA)
        self.masterTab.add(self.tab_camera, text="Cameras")
        # 4
        self.tab_presenter = self.initTabContent(TabType.PRESENTER)
        self.masterTab.add(self.tab_presenter, text="Presenters")
        #
        self.masterTab.select(self.tab_image)
        self.masterTab.enable_traversal()
    
    def updateMenu(self):
        self.menubar = MainMenu(self)
        self.parent.parent.config(menu=self.menubar)

    def initTabContent(self, tType):
        return MediaTab(self, tabType=tType, borderwidth=0, bg="#ccc")

    def hideToolbar(self):
        self.toolbar.pack_forget()
        self.updateMenu()

    def showToolbar(self):
        """"""
        self.toolbar = tk.Frame(self, relief=tk.FLAT, bg='#ccc')
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        #
        self.packLeftToolbar()
        if bool(store._get('FO100')):
            self.packRightToolbar()
    
    def packLeftToolbar(self):
        """"""
        lefToolbar = tk.Frame(self.toolbar, relief=tk.FLAT, bg='#ccc')
        lefToolbar.pack(side=tk.LEFT, fill=tk.Y)
        #
        # Creating a photoimage object to use image 
        photo = tk.PhotoImage(file=helper._ICONS_PATH+'ic_clock.png') 
        # Resizing image to fit on button 
        photoimage = photo.subsample(4,4) 
        # compound option is used to align image on LEFT side of button 
        schedule = tk.Button(lefToolbar, text=' Schedule', width=100, relief=tk.FLAT, image=photoimage, font=UI.TXT_FONT, compound=tk.LEFT, height=25, fg='#fff', bg='#ff2d55')
        schedule.photo = photoimage
        schedule.pack(side=tk.TOP, padx=10, pady=5) 
        
    def packRightToolbar(self):
        """"""
        rightToolbar = tk.Frame(self.toolbar, relief=tk.FLAT, bg='#ccc')
        rightToolbar.pack(side=tk.RIGHT, fill=tk.Y)
        #
        imgCheck = ImageTk.PhotoImage(Image.open(helper._ICONS_PATH+'close-pink.png'))
        lblCommandClear = tk.Label(rightToolbar, bd=1, image=imgCheck, bg="#ccc")
        lblCommandClear.photo = imgCheck
        lblCommandClear.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 15), pady=5)
        lblCommandClear.bind('<Button-1>', self.onClearResource)
        #
        imgCheck = ImageTk.PhotoImage(Image.open(helper._ICONS_PATH+'check-green.png'))
        lblCommandCheck = tk.Label(rightToolbar, bd=1, image=imgCheck, bg="#ccc")
        lblCommandCheck.photo = imgCheck
        lblCommandCheck.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0), pady=5)
        lblCommandCheck.bind('<Button-1>', self.onNewResource)
        #
        cbxData = {q170['NV106']: q170['FO100'] for q170 in self.loadCbxQ170()}
        cbxQ170 = LabeledCombobox(rightToolbar, cbxData, callback=self.onSelectBussiness, bd=1, relief=tk.FLAT)
        cbxQ170.pack(side=tk.RIGHT, padx=10, pady=10)
        #
        self.updateMenu()

    def onSelectBussiness(self, fo100):
        """"""
        self.FO100BU = fo100

    def onClearResource(self, evt):
        if messagebox.askyesno("PiepMe", "Are you sure to clear resource?"):
            pass
    def onNewResource(self, evt):
        if messagebox.askyesno("PiepMe", "Are you sure to renew resource?"):
            lsL500 = self.loadLsL500(self.FO100BU)
            presenter = list(filter(lambda l500: l500['LN508'] == 1, lsL500))
            camera = list(filter(lambda l500: l500['LN508'] == 0, lsL500))

    def loadCbxQ170(self):
        q170 = Q170_model()
        rs = q170.getListProviderWithRole({
            'FO100': store._get('FO100') or 0,
            'FQ180': Q180.CAM_LIV_OOF
        })
        return rs[WS.ELEMENTS] if rs[WS.STATUS] == WS.SUCCESS else []
        

    def loadLsL500(self, fo100):
        l500 = L500_model()
        rs = l500.l2019_listoftabL500_prov({
            'FO100': fo100,  # ID của DN
            'FO100M': 0,  # ID của member (BTV)
            'PL500': 0,  # ID Link
            'SORT': 1,  # 1: Cũ nhất, -1: Mới nhất
            'OFFSET': 0,
            'LIMIT': 200,
            'LOGIN': 'PiepLive Center'
        })
        return rs[WS.ELEMENTS] if rs[WS.STATUS] == WS.SUCCESS else []
