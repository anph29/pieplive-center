import cv2
import sys
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from ffpyplayer.player import MediaPlayer


class PThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent, **kwargs):
        super(PThread, self).__init__(parent)
        self.url = kwargs['url']
        self.mtype = kwargs['type']
        self.vH = kwargs['vH']
        self.vW = kwargs['vW']
        self.capture = cv2.VideoCapture(self.url)
        self.timeInterval = 1000 / (self.capture.get(cv2.CAP_PROP_FPS) or -1)

    def __del__(self):
        self.wait()

    def timelap(self):
        self.timer.setInterval(self.timeInterval)
        ret, frame = self.capture.read()
        if ret:.
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            pix = convertToQtFormat.scaled(self.vH, self.vW, QtCore.Qt.KeepAspectRatio)
            self.changePixmap.emit(pix)

    def run(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timelap)
        self.timer.start(self.timeInterval)


class QtCv2Cameta(QtWidgets.QWidget):
    vH = 135
    vW = 240

    def __init__(self, **kwargs):
        super().__init__()
        self.setData(kwargs)
        self.initUI()

    def initUI(self):
        self.itemCam = uic.loadUi("./src/ui/item_cam_cv2.ui", self)
        th = PThread(self, **self.getData())
        th.changePixmap.connect(self.setImage)
        th.start()

    def setData(self, input):
        self.name = input['name']
        self.url = input['url']
        self.mtype = input['type']

    def getData(self):
        return {
            'name': self.name,
            'url': self.url,
            'type': self.mtype,
            'vH': self.vH,
            'vW': self.vW
        }

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.itemCam.cv2_holder.resize(self.vH, self.vW)
        self.itemCam.cv2_holder.setPixmap(QtGui.QPixmap.fromImage(image))
