import tkinter as tk
from . import helper


def makePiepMePopup(title, geo):
    pmPopup = tk.Toplevel(padx=20, pady=10)
    pmPopup.wm_title(title)
    pmPopup.geometry(geo)
    imgicon = tk.PhotoImage(file=helper._LOGO_PATH)
    pmPopup.tk.call('wm', 'iconphoto', pmPopup._w, imgicon)
    pmPopup.resizable(0, 0)
    pmPopup.attributes('-topmost', 'true')

    return pmPopup
