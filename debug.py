#!/usr/bin/env python

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import os
from appIcons import Icons

def webcloseevent(event):
    print("sadkoawdawpd")
    print(event)

app = QApplication(sys.argv)

web = QWebView()
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "WhatsAppGui/index_8467.html"))
web.setMinimumSize(QtCore.QSize(800,900))
web.setMaximumSize(QtCore.QSize(800,900))
web.setWindowTitle("Mesaj Önizleme")
web.setWindowIcon(QtGui.QIcon(Icons["Standart"]))
web.load(QUrl.fromLocalFile(file_path))
web.show()

web.closeEvent = webcloseevent

sys.exit(app.exec_())