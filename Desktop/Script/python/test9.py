from PyQt5.QtWidgets import QApplication, QDialog,QWidget, QFileDialog, QPushButton, QLineEdit, QGridLayout
import sys
import os


class FileDialog(QDialog):
    def __init__(self):
        super(FileDialog,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QFileDialog")
        self.setGeometry(400,400,300,260)

        self.fileButton = QPushButton("文件对话框")
        self.fileLineEdit = QLineEdit()
        self.fileButton.clicked.connect(lambda:self.openFile(self.fileLineEdit.text()))

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.fileButton,0,0)
        self.mainLayout.addWidget(self.fileLineEdit,0,1)

        self.setLayout(self.mainLayout)

    def openFile(self,filePath):
        if os.path.exists(filePath):
            path = QFileDialog.getOpenFileName(self,"Open File Dialog",filePath,"Python files(*.py);;Text files(*.txt)")
        else:
            path = QFileDialog.getOpenFileName(self,"Open File Dialog","/","Python files(*.py);;Text files(*.txt)")

        self.fileLineEdit.setText(str(path[0]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileDialog()
    ex.show()
    sys.exit(app.exec_()) 
