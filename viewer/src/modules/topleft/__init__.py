import tkinter as tk
import vlc
import subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageGrab
#import win32gui

class TopLeft(tk.PanedWindow):
    def __init__(self, parent, *args, **kwargs):
        super(TopLeft, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.isStream = False
        self.pipe = None

        self.mainpanel = tk.Frame(self.parent)
        self.mainpanel.place(relheight=1, relwidth=1,x=0,y=0)#fill=tk.BOTH,expand=1

        self.Instance = vlc.Instance(['--video-on-top'])

        self.player = self.Instance.media_player_new()
        self.videopanel = tk.Frame(self.mainpanel)
        self.videopanel.place(relheight=1, relwidth=1,x=0,y=0)
        self.player.set_mrl("rtsp://viewer:FB1D2631C12FE8F7EE8951663A8A108@113.176.112.174:554", "network-caching=300")
        self.player.audio_set_mute(True)
        self.player.play()
        self.player.set_hwnd(self.videopanel.winfo_id())

        self.player1 = self.Instance.media_player_new()
        self.videopanel1 = tk.Frame(self.mainpanel)
        self.videopanel1.place(relheight=0, relwidth=0,x=0,y=0)
        self.player1.set_mrl("rtsp://viewer:FB1D2631C12FE8F7EE8951663A8A108@14.241.245.161:554", "network-caching=300")
        self.player1.audio_set_mute(True)
        self.player1.play()
        self.player1.set_hwnd(self.videopanel1.winfo_id())
        
        self.player2 = self.Instance.media_player_new()
        self.videopanel2 = tk.Frame(self.mainpanel)
        self.videopanel2.place(relheight=0, relwidth=0,x=0,y=0)
        self.player2.set_mrl("rtsp://viewer:FB1D2631C12FE8F7EE8951663A8A108@117.3.2.18:554", "network-caching=300")
        self.player2.audio_set_mute(True)
        self.player2.play()
        self.player2.set_hwnd(self.videopanel2.winfo_id())   

    def change_video(self,index):
        self.videopanel.place(relheight=0, relwidth=0,x=0,y=0)
        self.videopanel1.place(relheight=0, relwidth=0,x=0,y=0)
        self.videopanel2.place(relheight=0, relwidth=0,x=0,y=0)
        if index == 1:
            self.videopanel.place(relheight=1, relwidth=1,x=0,y=0)
        elif index == 2:
            self.videopanel1.place(relheight=1, relwidth=1,x=0,y=0)
        elif index == 3:
            self.videopanel2.place(relheight=1, relwidth=1,x=0,y=0)
    
    def showText(self):
        pass
    
    def hideElement(self):
        pass

    def on_print(self):
        white = (255, 255, 255)
        green = (0,128,0)
        image1 = Image.new("RGB", (1280, 720), white)
        image1.show()

    def start_stream(self):
        # self.rect = win32gui.GetWindowRect(self.mainpanel.winfo_id())
        # self.im = ImageGrab.grab(self.rect)
        # self.isStream = True
        # self.command = ['ffmpeg-win/ffmpeg.exe',
        #         '-f', 'rawvideo', 
        #         '-pix_fmt', 'bgr24',#rgba#bgr24
        #         '-s', '{}x{}'.format(self.im.width,self.im.height),
        #         '-i','-',
        #         '-i','src/musics/khi-long-ta-hieu.mp3',
        #         '-vb','250k',
        #         '-r','30',
        #         '-g','30',
        #         '-f','flv',
        #         'rtmp://livevn.piepme.com/cam/7421.bf586e24e22cfc1a058ba9e8cf96afee?token=bf586e24e22cfc1a058ba9e8cf96afee&SRC=WEB&FO100=7421&PL300=7940&LN301=180&LV302=115.73.208.139&LV303=0982231325&LL348=1554461547035&UUID=247cbf2ee3f0bda1&NV124=vn&PN303=15&POS=1']

        # self.pipe = subprocess.Popen(self.command, stdin=subprocess.PIPE)
        # self.stream()
        pass

    def stream(self):
        self.rect = win32gui.GetWindowRect(self.mainpanel.winfo_id())
        self.im = ImageGrab.grab(self.rect)
        img_np = np.array(self.im,dtype=np.uint8)
        self.pipe.stdin.write(img_np.tobytes())
        if self.isStream:
            self.after(30, self.stream)
    
    def stop_stream(self):
        self.isStream = False
        self.pipe.kill()
    