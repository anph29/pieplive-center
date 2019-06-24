import sys
import vlc
from PyQt5.QtWidgets import QPalette, QColor, QLabel

# In this widget, the video will be drawn
if sys.platform == "darwin":  # for MacOS
    from PyQt5.QtWidgets import QMacCocoaViewContainer as QFrames
else:
    from PyQt5.QtWidgets import QFrame as QFrames


class QMediaBox(QFrames):
    def __init__(self, camera=None, *args, **kwargs):
        super(QMediaBox, self).__init__(*args, **kwargs)
        self.set_data(camera)
        self.initGUI()

    def get_data(self):
        return {'name': self.name, 'url': self.url, 'type': self.mtype}

    def set_data(self, camera):
        self.name = camera['name']
        self.url = camera['url']
        self.mtype = camera['type']

    def initGUI(self):
        self.initTOP()
        self.initBOTTOM()

    def initTOP(self):
        self.palette = self.palette()
        self.palette.setColor(QPalette.Window,
                              QColor(0, 0, 0))
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

        self.Instance = vlc.Instance()
        media = self.Instance.media_new(self.url)
        player = self.Instance.media_player_new()
        player.set_media(media)
        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.winId())
        elif sys.platform == "win32":  # for Windows
            self.mediaplayer.set_hwnd(self.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.mediaplayer.set_nsobject(int(self.winId()))
        player.play()

    def initBOTTOM(self):
        # name
        self.addWidget(QLabel(self.name))
