from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from .appIcons import Icons

def warnMessage(title,iconType,text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setIcon(iconType)
    msg.setWindowIcon(QIcon(Icons["Standart"]))
    msg.setWindowFlags(Qt.WindowStaysOnTopHint)
    msg.setText(text)
    
    x = msg.exec_()