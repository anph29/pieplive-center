import PyQt5.QtWidgets as qtw


class QRightView(qtw.QGroupBox):

    def __init__(self, parent, *args, **kwargs):
        super(QRightView, self).__init__(parent, *args, **kwargs)

    def createGridLayout(self):
        self.horizontalGroupBox = qtw.QGroupBox("Grid")
        layout = qtw.QGridLayout()
        # layout.setColumnStretch(1, 4)
        # layout.setColumnStretch(2, 4)

        layout.addWidget(qtw.QPushButton('9'), 2, 2)# Cols - Rows

        self.horizontalGroupBox.setLayout(layout)
