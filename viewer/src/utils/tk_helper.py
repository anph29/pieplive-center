import tkinter as tk
from . import  helper

def makePiepMePopup(title, w=300, h=200):
    x = helper.getCenterX(w)
    y = 100
    pmPopup = tk.Toplevel(padx=20, pady=10)
    pmPopup.wm_title(title)
    pmPopup.geometry(f"{w}x{h}+{x}+{y}")
    imgicon = tk.PhotoImage(file=helper._LOGO_PATH)
    pmPopup.tk.call('wm', 'iconphoto', pmPopup._w, imgicon)
    pmPopup.resizable(0, 0)
    pmPopup.attributes('-topmost', 'true')

    return pmPopup
