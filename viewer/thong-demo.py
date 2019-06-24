import sys
import vlc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import subprocess
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.sizeHint = lambda: QSize(1280, 900)
        self.move(100, 10)
        self.mainFrame = QFrame()
        self.setCentralWidget(self.mainFrame)
        t_lay_parent = QHBoxLayout()
        t_lay_parent.setContentsMargins(0, 0, 0, 0)

        self.videoFrame = QFrame()
        self.videoFrame.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        t_lay_parent.addWidget(self.videoFrame)
        self.vlcInstance = vlc.Instance(['--video-on-top'])
        self.videoPlayer = self.vlcInstance.media_player_new()
        self.videoPlayer.video_set_mouse_input(False)
        self.videoPlayer.video_set_key_input(False)
        self.videoPlayer.set_mrl("https://youtu.be/hIDlwLM9o0k")
        self.videoPlayer.audio_set_mute(True)
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.videoPlayer.set_xwindow(self.videoFrame.winId())
        elif sys.platform == "win32": # for Windows
            self.videoPlayer.set_hwnd(self.videoFrame.winId())
        elif sys.platform == "darwin": # for MacOS
            self.videoPlayer.set_nsobject(int(self.videoFrame.winId()))

        self.videoPlayer.play()

        self.videoFrame1 = QFrame()
        t_lay_parent.addWidget(self.videoFrame1)
        self.videoFrame1.mouseDoubleClickEvent = self.mouseDoubleClickEvent1
        self.vlcInstance1 = vlc.Instance(['--video-on-top'])
        self.videoPlayer1 = self.vlcInstance1.media_player_new()
        self.videoPlayer1.video_set_mouse_input(False)
        self.videoPlayer1.video_set_key_input(False)
        self.videoPlayer1.set_mrl("rtsp://viewer:FB1D2631C12FE8F7@113.160.235.253:554", "network-caching=300")
        self.videoPlayer1.audio_set_mute(True)
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.videoPlayer1.set_xwindow(self.videoFrame1.winId())
        elif sys.platform == "win32": # for Windows
            self.videoPlayer1.set_hwnd(self.videoFrame1.winId())
        elif sys.platform == "darwin": # for MacOS
            self.videoPlayer1.set_nsobject(int(self.videoFrame1.winId()))
        self.videoPlayer1.play()

        print('asd')
        self.videoFrame2 = QFrame()
        t_lay_parent.addWidget(self.videoFrame2)
        self.videoFrame2.mouseDoubleClickEvent = self.mouseDoubleClickEvent2
        self.vlcInstance2 = vlc.Instance(['--video-on-top'])
        self.videoPlayer2 = self.vlcInstance2.media_player_new()
        self.videoPlayer2.video_set_mouse_input(False)
        self.videoPlayer2.video_set_key_input(False)
        self.videoPlayer2.set_mrl("rtsp://viewer:FB1D2631C12FE8F7@14.241.131.216:553", "network-caching=300")
        self.videoPlayer2.audio_set_mute(True)
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.videoPlayer2.set_xwindow(self.videoFrame2.winId())
        elif sys.platform == "win32": # for Windows
            self.videoPlayer2.set_hwnd(self.videoFrame2.winId())
        elif sys.platform == "darwin": # for MacOS
            self.videoPlayer2.set_nsobject(int(self.videoFrame2.winId()))
        self.videoPlayer2.play()
        
        buttonw = QPushButton("aaa")
        buttonw.setToolTip('This is an example button')
        buttonw.move(100,70)
        buttonw.clicked.connect(self.thong)
        t_lay_parent.addWidget(buttonw)
        
        self.mainFrame.setLayout(t_lay_parent)
        self.show()
        print('asd')

    def thong(self, event):
        screen = QApplication.primaryScreen()
        im = screen.grabWindow(self.mainFrame.winId())
        self.command = ['ffmpeg-win/ffmpeg.exe',
                '-f', 'rawvideo', 
                '-pix_fmt', 'bgr24',#rgba#bgr24
                '-s', '{}x{}'.format(im.width(),im.height()),
                '-i','-',
                '-i','src/musics/cau-chuyen-dem-v1.mp3',
                '-vb','250k',
                '-r','30',
                '-g','30',
                '-f','flv',
                'rtmp://livevn.piepme.com/cam/7421.bf586e24e22cfc1a058ba9e8cf96afee?token=bf586e24e22cfc1a058ba9e8cf96afee&SRC=WEB&FO100=7421&PL300=7940&LN301=180&LV302=115.73.208.139&LV303=0982231325&LL348=1554461547035&UUID=247cbf2ee3f0bda1&NV124=vn&PN303=15&POS=1']

        self.pipe = subprocess.Popen(self.command, stdin=subprocess.PIPE)
        self.my_timer = QTimer()
        self.my_timer.timeout.connect(self.stream)
        self.my_timer.start(30) #1 second interval
    
    def stream(self):
        #self.wpCpuUsage.display(cpu_percent(interval=1))
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.mainFrame.winId())
        #im =screenshot.toImage()
        

        screenshot.save('shot.jpg', 'jpg')
        #img_np = np.array(im,dtype=np.uint8)
        #self.pipe.stdin.write(im.bits())
        self.my_timer.start(1000)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.windowState() == Qt.WindowNoState:
                self.videoFrame1.hide()
                self.videoFrame.show()
                self.setWindowState(Qt.WindowFullScreen)
            else:
                self.videoFrame1.show()
                self.setWindowState(Qt.WindowNoState)

    def mouseDoubleClickEvent1(self, event):
        if event.button() == Qt.LeftButton:
            if self.windowState() == Qt.WindowNoState:
                self.videoFrame.hide()
                self.videoFrame1.show()
                self.setWindowState(Qt.WindowFullScreen)
            else:
                self.videoFrame.show()
                self.setWindowState(Qt.WindowNoState)

    def mouseDoubleClickEvent2(self, event):
        if event.button() == Qt.LeftButton:
            if self.windowState() == Qt.WindowNoState:
                self.videoFrame.hide()
                self.videoFrame2.show()
                self.setWindowState(Qt.WindowFullScreen)
            else:
                self.videoFrame.show()
                self.setWindowState(Qt.WindowNoState)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("VLC Test")

    window = MainWindow()
    app.exec_()