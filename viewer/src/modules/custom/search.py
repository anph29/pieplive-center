import tkinter as tk
import PIL
from PIL import ImageTk, Image
from .tooltip import ToolTip
from src.utils import helper


class ZSearch:
    def __init__(
        self,
        master,
        searchBg=None,
        getListFunc=None,
        clearViewFunc=None,
        renderFunc=None,
        pvSearchWidth=40,
        pvSearchColor=None,
        *agrs,
        **kwagrs,
    ):
        self.master = master
        self.searchBg = searchBg
        self.getListFunc = getListFunc
        self.clearViewFunc = clearViewFunc
        self.renderFunc = renderFunc
        self.pvSearchWidth = pvSearchWidth
        self.pvSearchColor = pvSearchColor
        self.initUI()

    def initUI(self):
        self.pvSearch = tk.StringVar()
        self.pvSearch.trace("w", self.doSearch)
        self.searchZone = tk.Frame(self.master, bg=self.searchBg)
        # eSearch
        eSearch = tk.Entry(
            self.searchZone,
            bg=self.pvSearchColor or self.searchBg,
            textvariable=self.pvSearch,
            width=self.pvSearchWidth,
            borderwidth=5,
            relief=tk.FLAT,
        )
        eSearch.pack(side=tk.LEFT, padx=15, pady=5)
        # clear search
        imgClear = ImageTk.PhotoImage(Image.open(f"{helper._ICON_PATH}ic-clear.png"))
        self.cmdClear = tk.Label(
            self.searchZone, image=imgClear, cursor="hand2", bg=self.searchBg
        )
        self.cmdClear.image = imgClear
        self.cmdClear.bind("<Button-1>", self.doClearSearch)
        ToolTip(self.cmdClear, "clear search")
        # btn search
        imgSearch = ImageTk.PhotoImage(Image.open(f"{helper._ICON_PATH}ic-search.png"))
        cmdSearch = tk.Label(
            self.searchZone, image=imgSearch, cursor="hand2", bg=self.searchBg
        )
        cmdSearch.image = imgSearch
        cmdSearch.bind("<Button-1>", self.doSearch)
        cmdSearch.pack(side=tk.RIGHT, pady=5, padx=(0, 15))
        ToolTip(cmdSearch, "search")

    def doClearSearch(self, evt):
        self.cmdClear.pack_forget()
        self.pvSearch.set("")
        self.clearViewFunc()
        self.renderFunc(self.getListFunc())

    def doSearch(self, *agrs):
        txtSearch = helper.removeUnicode(self.pvSearch.get().strip().lower())
        if len(txtSearch) == 0:
            self.doClearSearch(None)
        else:
            self.cmdClear.pack(side=tk.RIGHT, pady=5, padx=(5, 5))
            self.clearViewFunc()
            allMedia = self.getListFunc()
            filtered = list(
                filter(
                    lambda x: txtSearch in helper.removeUnicode(x["name"].lower()),
                    allMedia,
                )
            )
            self.renderFunc(filtered)
