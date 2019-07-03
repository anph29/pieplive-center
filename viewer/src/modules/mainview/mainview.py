import tkinter as tk
from tkinter import ttk
from src.utils import helper, store
from src.modules.mediatab import MediaTab, TabType
from src.models import Q170_model, L500_model
from src.enums import Q180
from src.modules.custom import LabeledCombobox
from PIL import Image, ImageTk
from src.modules.menu import MainMenu
from uuid import getnode as get_mac


class MainView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MainView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.after(100, self.initGUI)

    def set_style(self):
        style = ttk.Style()
        style.theme_create("TabStyle", parent="alt", settings={
            "TNotebook": {
                "configure": {"tabmargins": [10, 0, 0, 10]}  # L T B R
            },
            "TNotebook.Tab": {
                "configure": {"padding": [15, 5, 15, 5]}
            }
        })
        style.theme_use("TabStyle")

    def initGUI(self):
        self.set_style()
        #
        self.updateMenu()
        #
        if bool(store._get('FO100')):
            self.showToolbar()
        #
        self.masterTab = ttk.Notebook(self)
        self.masterTab.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        #
        self.tab_custom = self.initTabContent(TabType.CUSTOM)
        self.masterTab.add(self.tab_custom, text="Custom Resource")
        #
        self.tab_camera = self.initTabContent(TabType.CAMERA)
        self.masterTab.add(self.tab_camera, text="Camera")
        #
        self.tab_presenter = self.initTabContent(TabType.PRESENTER)
        self.masterTab.add(self.tab_presenter, text="Presenter")
        #
        self.masterTab.select(self.tab_camera)
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
        self.toolbar = tk.Frame(self, relief=tk.FLAT, bg='#ccc')
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        #
        imgCheck = ImageTk.PhotoImage(Image.open(helper._ICONS_PATH+'close-pink.png'))
        lblCommandClear = tk.Label(self.toolbar, image=imgCheck, bg="#ccc")
        lblCommandClear.photo = imgCheck
        lblCommandClear.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=5)
        lblCommandClear.bind('<Button-1>', self.onClearResource)
        #
        imgCheck = ImageTk.PhotoImage(Image.open(helper._ICONS_PATH+'check-green.png'))
        lblCommandCheck = tk.Label(self.toolbar, image=imgCheck, bg="#ccc")
        lblCommandCheck.photo = imgCheck
        lblCommandCheck.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0), pady=5)
        lblCommandCheck.bind('<Button-1>', self.onNewResource)
        #
        cbxData = {q170['NV106']: q170['FO100'] for q170 in self.loadCbxQ170()}
        cbxQ170 = LabeledCombobox(self.toolbar, cbxData, callback=self.loadMediaByFO100BU, bd=1, relief=tk.FLAT)
        cbxQ170.pack(side=tk.RIGHT, padx=10, pady=10)
        #
        self.updateMenu()

    def onClearResource(self):
        
    def onNewResource(self):
        

    def loadMediaByFO100BU(self, fo100):
        self.loadLsL500(fo100)

    def loadCbxQ170(self):
        q170 = Q170_model()
        rs = q170.getListProviderWithRole({
            'FO100': store._get('FO100') or 0,
            'FQ180': Q180.CAM_LIV_OOF
        })
        return rs['elements'] if rs['status'] == 'success' else []
        

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
        return rs['elements'] if rs['status'] == 'success' else []
