import tkinter as tk
from src.modules.topleft import TopLeft
from src.modules.bottomleft import BottomLeft


class LeftView(tk.PanedWindow):
    def __init__(self, parent, *args, **kwargs):
        super(LeftView, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.i = 0
        self.init_layout()

    def init_layout(self):
        self.top = TopLeft(self, bg='#0F0')
        self.top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.bottom = BottomLeft(self, height=160, bg='#F18A16')
        self.bottom.pack(side=tk.BOTTOM, fill=tk.X)

        self.control = tk.PanedWindow(self, height=40, bg='#F00')
        self.init_control()
        self.control.pack(side=tk.BOTTOM, fill=tk.X)
    
    def init_control(self):
        btn_start  = tk.Button(self.control, text="Stream", command=self.start_stream)
        btn_stop  = tk.Button(self.control, text="Stop", command=self.stop_stream)
        btn_change  = tk.Button(self.control, text="Change", command=self.change)
        btn_print  = tk.Button(self.control, text="Print", command=self.on_print)
        btn_start.pack(side=tk.LEFT)
        btn_stop.pack(side=tk.LEFT)
        btn_change.pack(side=tk.LEFT)
        btn_print.pack(side=tk.LEFT)

    def start_stream(self):
        print('StartStream')
        self.top.start_stream()

    def stop_stream(self):
        print('StopStream')
        self.top.stop_stream()

    def change(self):
        if self.i == 3:
            self.i=0
        self.i +=1
        print('change')
        self.top.change_video(self.i)
        
        # self.top.change_video( {
        #     "name": "H\u1ed9i An",
        #     "url": "rtsp://viewer:FB1D2631C12FE8F7EE8951663A8A108@113.176.112.174:554",
        #     "type": "RTSP"
        # })

    def on_print(self):
        self.top.on_print()