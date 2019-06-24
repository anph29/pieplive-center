import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication
from src.modules.custom import QtCameta, QtCv2Cameta
from src.utils import helper
import math


class PiepMe(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        piepme = uic.loadUi("./src/ui/piepme.ui", self)
        self.initTabCamera(piepme.grid_camera)

    def initTabCamera(self, target):
        row = 0
        for num, cam in enumerate(helper._load_lscam()):
            row = math.floor(num / 5)
            target.addWidget(QtCameta(**cam), row, num % 5)

    def initTabPresenter(self, target):
        row = 0
        for num, cam in enumerate(helper._load_ls_presenter()):
            row = math.floor(num / 5)
            target.addWidget(QtCameta(**cam), row, num % 5)


def run():
    app = QApplication(sys.argv)
    piepme = PiepMe()
    piepme.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
