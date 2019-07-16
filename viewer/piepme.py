import tkinter as tk
from src.modules.mainview import MainView
from src.utils import helper, store, tk_helper, zip_helper

class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.after(100, self.initGUI)

    def initGUI(self):
        self.mainview = MainView(self, borderwidth=0, bg='#000')
        self.mainview.pack(fill=tk.BOTH, expand=True)

def run():
    root = tk.Tk()
    w = 1280
    x = tk_helper.getCenterX(w)
    root.geometry(f"{w}x900+{x}+20")
    root.title("PiepLive Center Setting")
    imgicon = tk.PhotoImage(file=helper._LOGO_VIEWER)
    root.tk.call('wm', 'iconphoto', root._w, imgicon)
    MainApplication(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    helper.makeSureResourceFolderExisted()
    run()

   