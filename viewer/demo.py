

from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import sys


class VideoPlayer:


    video_path = "https://livevn.piepme.com/camhls/14789.a6a2cdaedb0e4a62b8307d232370f4ff_720p/index.m3u8"

    def __init__(self):
        self.video = QVideoWidget()
        self.video.resize(640, 480)
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video)
        self.player.setMedia(QMediaContent(
            QUrl.fromUserInput(self.video_path)))
        self.player.setPosition(0)  # to start at the beginning of the video every time
        self.video.show()
        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = VideoPlayer()
    sys.exit(app.exec_())
