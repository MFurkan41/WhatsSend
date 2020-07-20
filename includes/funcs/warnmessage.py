def warnMessage(title,iconType,text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setIcon(iconType)
    msg.setWindowIcon(QtGui.QIcon(Icons["Standart"]))
    msg.setText(text)
    
    x = msg.exec_()