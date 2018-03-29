from PyQt5.QtWidgets import QApplication, QDialog,QWidget, QColorDialog, QPushButton, QGridLayout, QFrame
from PyQt5.QtGui import QPalette,QColor
import sys
from PyQt5.QtCore import Qt


class ColorDialog(QDialog):
    def __init__(self):
        super(ColorDialog,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ColorDialog")
        self.setGeometry(400,400,300,260)

        self.colorButton = QPushButton("颜色对话框")
        self.colorFrame = QFrame()
        self.colorFrame.setFrameShape(QFrame.Box)
        self.colorFrame.setAutoFillBackground(True)
        self.colorButton.clicked.connect(self.openColor)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.colorButton,0,0)
        self.mainLayout.addWidget(self.colorFrame,0,1)

        self.setLayout(self.mainLayout)

    def openColor(self):
        color = QColorDialog.getColor(Qt.white,None,"Selectting Color")
        if color.isValid():
            self.colorFrame.setPalette(QPalette(color))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ColorDialog()
    ex.show()
    sys.exit(app.exec_()) 
