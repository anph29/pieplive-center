# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk

from src.modules.menu.mainmenu import MainMenu
from src.modules.rightview import RightView


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        MainMenu(self.parent)
        self.after(100, self.init_layout)

    def init_layout(self):
        right = RightView(self, borderwidth=0, bg='#000')
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x900+30+20")
    root.title("PiepLive Center V2")
    imgicon = tk.PhotoImage(file="../resource/icons/logo-viewer.png")
    root.tk.call('wm', 'iconphoto', root._w, imgicon)
    MainApplication(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
