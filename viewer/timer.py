import cv2
import sys
from PyQt5 import QtCore, QtWidgets
from time import strftime


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)
        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.display(strftime("%S"))
        self.setCentralWidget(self.lcd)
        self.setGeometry(300, 300, 250, 100)

    def Time(self):
        self.timer.setInterval(1000)
        self.lcd.display(strftime("%S"))


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


class QTCamera():
    def __init__(self):
        self.initUI()

    def initUI(self):
        pass
