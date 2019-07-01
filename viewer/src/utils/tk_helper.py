import tkinter as tk
from . import  helper
import ctypes


def makePiepMePopup(title, w=300, h=200):
    x = getCenterX(w)
    y = 100
    pmPopup = tk.Toplevel(padx=20, pady=10)
    pmPopup.wm_title(title)
    pmPopup.geometry(f"{w}x{h}+{x}+{y}")
    imgicon = tk.PhotoImage(file=helper._LOGO_VIEWER)
    pmPopup.tk.call('wm', 'iconphoto', pmPopup._w, imgicon)
    pmPopup.resizable(0, 0)
    pmPopup.attributes('-topmost', 'true')

    return pmPopup

def getCenterX(w):
    user32 = ctypes.windll.user32
    screen_w = user32.GetSystemMetrics(0)
    return int(screen_w / 2 - w / 2)