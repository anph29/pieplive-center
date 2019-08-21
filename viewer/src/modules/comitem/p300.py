import tkinter as tk
import requests
import urllib
from io import BytesIO
from src.utils import helper, store
from src.constants import UI, WS
from src.models import L300_model
from src.modules.custom import PLabel, ToolTip
from uuid import getnode
from PIL import ImageTk, Image
from src.utils import scryto
import urllib
import sys
from datetime import datetime, timedelta
import time


class P300(tk.Frame):
    def __init__(self, parent, p300=None, parentTab=None, *args, **kwargs):
        super(P300, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parentTab = parentTab
        self.cell_width = 360
        self.top_height = 203
        self.bot_height = 25
        self.botBg = "#F4ECF7"
        self.p300 = p300
        self.setData(p300)

        self.initGUI()

    def setData(self, p300):
        self.PP300 = self.p300["PP300"] if "PP300" in p300 else 0
        self.PV301 = self.p300["PV301"] if "PV301" in p300 else ""
        self.PN303 = self.p300["PN303"] if "PN303" in p300 else 0
        self.PV307 = self.p300["PV307"] if "PV307" in p300 else ""
        self.PO322 = self.p300["PO322"] if "PO322" in p300 else {}
        self.FT300 = self.p300["FT300"] if "FT300" in p300 else 0
        if "live" in self.PO322:
            self.liveTime = datetime.strptime(
                self.PO322["live"]["time"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )

    def initGUI(self):
        ww = self.cell_width + 5
        wh = 5 + self.top_height + self.bot_height
        self.wrapper = tk.Frame(
            self, relief=tk.FLAT, bd=1, bg="#fff", width=ww, height=wh
        )
        self.wrapper.pack(fill=tk.BOTH)
        self.initTOP()
        self.initBOTTOM()

    def initTOP(self):
        self.top = tk.Frame(
            self.wrapper,
            bd=0,
            relief=tk.FLAT,
            bg="#999",
            width=self.cell_width,
            height=self.top_height,
        )
        self.top.pack(side=tk.TOP)
        try:
            response = requests.get(self.PV307)
            im = Image.open(BytesIO(response.content))
        except requests.exceptions.MissingSchema:
            im = Image.open(helper._IMAGES_PATH + "splash2.png")
        #
        nW, nH, pdx, pdy = self.calcSizeAndPad(im.size)
        resized = im.resize((nW, nH), Image.ANTIALIAS)
        imgMedia = ImageTk.PhotoImage(resized)
        self.topImage = tk.Label(self.top, image=imgMedia, bg="#f2f2f2", cursor="hand2")
        self.topImage.photo = imgMedia
        #
        self.topImage.pack(padx=pdx, pady=pdy)

    def calcSizeAndPad(self, size):
        """
        if showFrame is `vertical`:
            if ratio(h) > :9:
                `calcByH`
            else:
                `calcByW`
        elif showFrame is `horizontal`:
            if ratio(w) > :16:
                `calcByW`
            else:
                `calcByH`
        """
        w, h = size
        r = w / h
        if w > h and r >= 16 / 9:
            return self.calcSizeByWidth(r)
        else:
            return self.calcSizeByHeight(r)

    def calcSizeByWidth(self, r):
        nW = self.cell_width
        nH = int(nW / r)
        pdx = 0
        pdy = int((self.top_height - nH) / 2)
        return nW, nH, pdx, pdy

    def calcSizeByHeight(self, r):
        nH = self.top_height
        nW = int(nH * r)
        pdx = int((self.cell_width - nW) / 2)
        pdy = 0
        return nW, nH, pdx, pdy

    def initBOTTOM(self):
        self.bottom = tk.Frame(
            self.wrapper,
            bd=5,
            relief=tk.FLAT,
            bg=self.botBg,
            width=self.cell_width,
            height=self.bot_height,
        )
        self.bottom.pack(side=tk.BOTTOM, fill=tk.X)
        # label
        self.lbl_name = PLabel(
            self.bottom,
            text=urllib.parse.unquote(self.PV301),
            justify=tk.LEFT,
            elipsis=22,
            bg=self.botBg,
            font=UI.TXT_FONT,
            fg="#000",
        )
        ToolTip(self.lbl_name, urllib.parse.unquote(self.PV301))
        self.lbl_name.pack(side=tk.LEFT)

        if self.parentTab.keyManager.existedKey(self.PP300):
            self.packCheckExisted()
        else:  # not existed check least of 3 hrs
            threeHrs = 3 * 60 * 60
            if self.getDifferenceTimeFromNowToLive() <= threeHrs:
                self.packBtnGetKey()
            else:
                self.packWaitTimeGetKey()

    def getDifferenceTimeFromNowToLive(self):
        now = datetime.utcnow().timestamp()
        live = self.liveTime.timestamp()
        return live - now

    def packBtnGetKey(self):
        # get key
        self.btnGetKey = tk.Button(
            self.bottom,
            text="Get Key",
            relief=tk.FLAT,
            command=self.genarateKeyAndSave,
            font=UI.TXT_FONT,
            cursor="hand2",
            bg="#ff2d55",
            fg="#fff",
        )
        self.btnGetKey.configure(width=7)
        self.btnGetKey.pack(side=tk.RIGHT, padx=1, pady=1)

    def packCheckExisted(self):
        # already
        imChk = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}check-green-s.png"))
        self.lblExisted = tk.Label(
            self.bottom, image=imChk, cursor="hand2", bg=self.botBg
        )
        self.lblExisted.image = imChk
        self.lblExisted.pack(side=tk.RIGHT, padx=5, pady=5)
        ToolTip(self.lblExisted, "Already key")

    def packWaitTimeGetKey(self):
        offset = datetime.now() - datetime.utcnow()
        timeTooltip = self.liveTime - timedelta(hours=3) + offset
        timeTooltipStr = datetime.strftime(timeTooltip, "%d/%m/%Y %H:%M")
        # already
        imChk = ImageTk.PhotoImage(Image.open(f"{helper._ICONS_PATH}ic-wait.png"))
        self.lblExisted = tk.Label(
            self.bottom, image=imChk, cursor="hand2", bg=self.botBg, text="Waiting"
        )
        self.lblExisted.image = imChk
        self.lblExisted.pack(side=tk.RIGHT, padx=5, pady=5)
        ToolTip(self.lblExisted, "Can get key from: " + timeTooltipStr)

    def genarateKeyAndSave(self):
        if not self.parentTab.keyManager.existedKey(self.PP300):
            l300 = self.insertL300()
            URL, STREAMKEY = self.makeRTMP(l300)
            self.parentTab.saveKeyStream(
                {
                    "id": l300["PL300"],
                    "label": urllib.parse.unquote(self.PV301),
                    "key_a": URL,
                    "key_b": STREAMKEY,
                    "PLAY": l300["PLAY"],
                    "P300": self.p300,
                }
            )
        #
        self.btnGetKey.pack_forget()
        self.packCheckExisted()

    def insertL300(self):
        l300 = L300_model()
        ADDRESS, LAT, LONG = self.getLocation()
        liveObj = self.PO322["live"] if "live" in self.PO322 else {}
        fl300 = liveObj["FL300"] if "FL300" in liveObj else 0
        AV107 = store._get("NO133")["NV133_P"] if None != store._get("NO133") else ""

        rs = l300.live_inserttabL300(
            {
                "FO100": store.getCurrentActiveBusiness(),  # fo100 doanh nghiep
                "PN303": self.PN303,
                "LV302": helper.getMyIP(),  # IP
                "LV303": AV107,  # phone
                "FT300": self.FT300,
                "PL300": fl300,  # nếu đã có FL300 (đã lấy key) thì truyền lại FL300, (p300.PO322.live.FL300)
                "ADDRESS": ADDRESS,
                "LAT": LAT,
                "LONG": LONG,
                "UUID": hex(getnode()),  # UUID của thiết bị mobile
                "NV124": store._get("NV124"),  # Quốc Gia
                "SRC": "WEB",
                "pvLOGIN": store._get("NV101"),
            }
        )
        return rs[WS.ELEMENTS] if rs[WS.STATUS] == WS.SUCCESS else []

    def makeRTMP(self, l300):
        FO100BU = store.getCurrentActiveBusiness()
        ADDRESS, LAT, LONG = self.getLocation()
        URL = f'rtmp://{l300["EDGE"]}/{l300["APP"]}/'
        STREAMKEY = (
            f'{FO100BU}.{l300["TOKEN"]}?token={l300["TOKEN"]}&SRC=WEB&FO100={FO100BU}&PL300={l300["PL300"]}&LN301={l300["LN301"]}&LV302={l300["LV302"]}'
            + f'&LV303={l300["LV303"]}&LL348={l300["LL348"]}&UUID={hex(getnode())}&NV124={store._get("NV124")}'
            + (
                f"&PN303={self.p300['PN303']}"
                if self.PN303 == 15
                else f"&LAT={LAT}&LONG={LONG}"
            )
        )

        return URL, STREAMKEY

    def getLocation(self):
        locObj = (
            store._get("NO123")
            if store._get("NO123")
            else store._get("NO122")
            if store._get("NO122")
            else None
        )
        ADDRESS = locObj["ADDRESS"] if "ADDRESS" in locObj else ""
        LAT = locObj["coordinates"][1]
        LONG = locObj["coordinates"][0]
        return ADDRESS, LAT, LONG
