import tkinter as tk


def makePiepMePopup(title, geo):
    pmPopup = tk.Toplevel(padx=20, pady=10)
    pmPopup.wm_title(title)
    pmPopup.geometry(geo)
    imgicon = tk.PhotoImage(file="../resource/icons/logo-viewer.png")
    pmPopup.tk.call('wm', 'iconphoto', pmPopup._w, imgicon)
    pmPopup.resizable(0, 0)
    pmPopup.attributes('-topmost', 'true')

    return pmPopup
