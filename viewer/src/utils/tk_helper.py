import tkinter as tk
from . import helper
import ctypes
import re


def makePiepMePopup(title, w=300, h=200, padx=20, pady=10):
    x = getCenterX(w)
    y = 100
    pmPopup = tk.Toplevel(padx=padx, pady=pady)
    pmPopup.wm_title(title)
    pmPopup.geometry(f"{w}x{h}+{x}+{y}")
    imgicon = tk.PhotoImage(file=helper._LOGO_VIEWER)
    pmPopup.tk.call("wm", "iconphoto", pmPopup._w, imgicon)
    pmPopup.resizable(0, 0)
    pmPopup.attributes("-topmost", "true")

    return pmPopup


def getCenterX(w):
    user32 = ctypes.windll.user32
    screen_w = user32.GetSystemMetrics(0)
    return int(screen_w / 2 - w / 2)


def character_limit(strVar, limit=6):
    if len(strVar.get()) > limit:
        strVar.set(strVar.get()[0:limit])


def verifyHMS_val(strvar):
    character_limit(strvar, limit=2)
    strvar.set(re.sub(r"^[^0-9]{2}$", "", strvar.get()))


def getComboboxValueRange(end=60):
    return [(f"{x}", f"0{x}")[x < 10] for x in range(0, end)]
