from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import Classify
import  threading


class Ui_MainWindow(object):
    path = None
    file_list_mp3 = None
    progressBar = None
    model = None
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 312)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 20, 551, 31))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 441, 31))
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setStyleSheet(
            "QLabel { background-color : white; border-style: solid; border-width: 1px; border-color: black;}")

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(440, 0, 111, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pushButtonClicked)

        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(30, 60, 551, 191))
        self.listView.setObjectName("listView")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 260, 551, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.progressBar = QtWidgets.QProgressBar(self.widget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_2.clicked.connect(self.pushButton_2Clicked)


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Music Mood Classifier"))
        self.pushButton.setText(_translate("MainWindow", "Select Folder"))
        self.pushButton_2.setText(_translate("MainWindow", "Classify"))


    def pushButtonClicked(self):
        self.path = QFileDialog.getExistingDirectory()
        self.label.setText(self.path)
        file_list = os.listdir(self.path)
        self.file_list_mp3 = [file for file in file_list if file.endswith(".mp3")]
        self.model = QStandardItemModel()
        for mp3_files in self.file_list_mp3:
            self.model.appendRow(QStandardItem(mp3_files))
        self.listView.setModel(self.model)
        self.progressBar.setProperty("value", 0)


    def pushButton_2Clicked(self):
        self.threadclass = ThreadClass(self.path,self.file_list_mp3,self.progressBar,self.model)
        self.threadclass.start() 

class ThreadClass(threading.Thread):
    def __init__(self, path, file_list_mp3, progressBar,model):
        threading.Thread.__init__(self)
        self.path = path
        self.file_list_mp3 = file_list_mp3
        self.progressBar = progressBar
        self.model = model
    def run(self):
        Classify.Folder.makeFolders(self.path)
        Classify.ML.MoodClassify(self.path, self.file_list_mp3, self.progressBar,self.model)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

