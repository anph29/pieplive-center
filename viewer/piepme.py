import tkinter as tk
from src.modules.mainview import MainView
from src.utils import helper, store, tk_helper, zip_helper, firebase

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
    piepme = MainApplication(root)
    piepme.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def onStop():
        piepme.mainview.tab_presenter.stopListenerStream()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", onStop)
    root.mainloop()

def run1():
    firebase.setP300AfterStartStream(
        {
            "FO100": 1932,
            "FO100W": 4033,
            "FT300": 1,
            "PV301": "test%20count%20down",
            "PN303": 9,
            "PV307": "",
            "PD308": "2019-08-14T09:45:00.000Z",
            "PN309": 0,
            "PO322": {
                "live": {
                    "time": "2019-08-14T09:45:00.000Z",
                    "description": "",
                    "title": "test count down",
                    "FL300": 8923,
                    "src": "",
                    "NV124": "vn",
                }
            },
            "PO323": {
                "PN323_CMAP": 0,
                "PN323_RULE": 0,
                "PA323_SRE": ["OTH", "PME"],
                "PN323_FEE": 0,
                "PN323_DONA": 0,
                "PN323_NRC": 0,
                "PN323_CM": 1,
            },
            "PV325": "VWmgVqEMoWl",
            "PP300": 6641,
            "TYPE": "N100",
            "NV106": "Â  n",
            "NV126": "https://media.piepme.com/4033/images/avartaoohhay?t=1564930109622",
            "NV106W": "Â  n",
            "NV126W": "https://media.piepme.com/4033/images/avartaoohhay?t=1564930109622",
        }
    )

if __name__ == "__main__":
    helper.makeSureResourceFolderExisted()
    run()

   