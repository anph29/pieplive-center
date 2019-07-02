import os
import tkinter as tk
from src.modules.menu.mainmenu import MainMenu
from src.modules.rightview import RightView
from src.modules.login import Login
from src.utils import helper, store, tk_helper, zip_helper

class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        MainMenu(self.parent)
        self.after(100, self.init_layout)

    def init_layout(self):
        right = RightView(self, borderwidth=0, bg='#000')
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # if not lign
        if store._get('FO100') == None:
            login = Login(self.parent)
            login.open()


def run():
    root = tk.Tk()
    w = 1280
    x = tk_helper.getCenterX(w)
    root.geometry(f"{w}x900+{x}+20")
    root.title("PiepLive Center V2")
    imgicon = tk.PhotoImage(file=helper._LOGO_VIEWER)
    root.tk.call('wm', 'iconphoto', root._w, imgicon)
    MainApplication(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    existedResource = os.path.exists("../resource")
    if not existedResource:
        zip_helper.extractZip('./resource.zip', '../')
    run()

   