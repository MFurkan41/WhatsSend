# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSize, Qt, QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMenuBar, QStatusBar, QApplication, QMainWindow

from includes import *
from ..appIcons import Icons


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(380, 100)
        MainWindow.setMinimumSize(QSize(380, 100))
        MainWindow.setMaximumSize(QSize(380, 100))
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.centralwidget)
        font = QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 380, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setWindowIcon(QIcon(Icons["Standart"]))

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lütfen bekleyiniz..."))
        self.label.setText(_translate("MainWindow", "Sunucu ile bağlantı kurulmakta, lütfen bekleyiniz..."))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_()) 