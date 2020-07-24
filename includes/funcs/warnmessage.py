from PyQt5.QtWidgets import QMessageBox
from appIcons import Icons
from PyQt5 import QtGui,QtCore

def warnMessage(title,iconType,text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setIcon(iconType)
    msg.setWindowIcon(QtGui.QIcon(Icons["Standart"]))
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    msg.setText(text)
    
    x = msg.exec_()