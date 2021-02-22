from PyQt5 import QtCore, QtGui, QtWidgets
from appIcons import Icons


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.ScRate = GetSystemMetrics(0)/1920
        MainWindow.resize(552*self.ScRate, 368*self.ScRate)
        MainWindow.setMinimumSize(QtCore.QSize(552*self.ScRate, 368*self.ScRate))
        MainWindow.setMaximumSize(QtCore.QSize(552*self.ScRate, 368*self.ScRate))
        MainWindow.setWindowIcon(QtGui.QIcon(Icons["Standart"]))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 531, 301))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 552, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.checkBox.setDisabled(True)
        self.pushButton.setDisabled(True)
        self.textBrowser.verticalScrollBar().valueChanged.connect(self.checkRead)
        self.checkBox.stateChanged.connect(lambda val: self.pushButton.setDisabled(False) if val else(self.pushButton.setDisabled(True)))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def checkRead(self,val):
        if val == self.textBrowser.verticalScrollBar().maximum():
            self.checkBox.setDisabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Lorem Ipsum Dolor Sit Amet</span></p></body></html>"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.1</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Lorem ipsum dolor sit </span>amet, in sit illud prompta consetetur. Habemus eleifend vis no. Usu noster cetero nominati te, cu aeque urbanitas vix. No everti suscipiantur est, modo minimum nam ea, choro fabulas quo ne. Verear euismod adversarium id per, at errem delicata definiebas sed, duo sumo reque vivendum et. Te alia sint oblique nam<span style=\" font-weight:600;\">, ea omnis laoreet singulis qui.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.2</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Inani civibus ponderum mei id. Eripuit menandri principes pro ut, natum porro sadipscing cum ei. Eripuit corrumpit efficiantur per eu. Vel ut purto impedit senserit, his te adhuc nulla.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.3</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Eius epicurei ei eam, ius nemore consetetur at, duo ut omnis essent. Omnes fastidii est in. Enim eripuit molestiae vel eu. Quo no etiam mollis, invidunt interesset an ius. Sumo veri et est, vim imperdiet consetetur ad. Ea ius aliquip inermis.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.3.1</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Quo probo cotidieque in. Te mea falli accusata, an per modo vide. Cum cu nobis scaevola. Nominavi pertinax qui et, sit in fugit ocurreret. Utamur persecuti quo in, no mei saepe accusamus reprehendunt.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.4</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Est eruditi deseruisse scribentur et, pro ex audiam docendi voluptatum. Diceret adversarium cu pri, suas omnes tibique has ea, ea vidit delicatissimi pri. Cu mea summo dolore. Ei nostro luptatum per.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.5</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Errem eruditi vim ne. His volumus expetendis an, eam cu porro recteque. Noluisse quaestio corrumpit mea in. Ad mea mundi antiopam, accumsan quaestio laboramus at his.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Sed ipsum mazim iuvaret ut, ad utroque constituam persequeris sea. In audiam scripta tincidunt nam, duo ut summo mandamus. Praesent laboramus no has, vis tota scribentur ne. Has elit meis doming eu, usu adhuc assum forensibus et, et his malis tantas elaboraret. Delenit neglegentur ei mel. No mea aperiri deserunt convenire, usu facer erant eleifend ad.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.7</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">No sea minim gloriatur, cu mel nihil possit. An animal meliore vis. Nemore tincidunt intellegebat nam at. An eos duis quas, et mel nullam fabulas dolorem. Qui ut tempor ponderum luptatum, ut meliore vivendo necessitatibus sed, te feugiat impedit dissentiunt nam. Vel dolor imperdiet at, et his lucilius neglegentur.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.8</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Dicunt offendit vel ea, eum suscipit senserit constituam ex. Vim amet eleifend in, mea at quaeque dignissim urbanitas. Audire ancillae cum at, ei hinc repudiare pro. Saperet eleifend te nam, has quod dicta tempor cu.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">1.9</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">An duo viris eruditi epicuri. Pri nibh cibo argumentum an, vix discere deserunt et. Est cu veri sapientem periculis. Nam probo quaerendum voluptatibus te, cum recusabo vituperatoribus ad.</p></body></html>"))
        self.checkBox.setText(_translate("MainWindow", "Okudum, kabul ediyorum."))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_()) 