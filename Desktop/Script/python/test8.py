from PyQt5.QtWidgets import QApplication, QDialog,QWidget, QFontDialog, QPushButton, QLineEdit, QGridLayout
import sys
import os


class FontDialog(QDialog):
    def __init__(self):
        super(FontDialog,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QFontDialog")
        self.setGeometry(400,400,300,260)

        self.fontButton = QPushButton("字体选择对话框")
        self.fontLineEdit = QLineEdit("Hello Python")
        self.fontButton.clicked.connect(self.openFont)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.fontButton,0,0)
        self.mainLayout.addWidget(self.fontLineEdit,0,1)

        self.setLayout(self.mainLayout)

    def openFont(self):
         font,ok=QFontDialog.getFont()
         if ok:
            self.fontLineEdit.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FontDialog()
    ex.show()
    sys.exit(app.exec_())
