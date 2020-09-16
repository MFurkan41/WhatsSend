from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
import os
from appIcons import Icons


class WebViewBrowser(QtWidgets.QMainWindow):
    def __init__(self,rast):
        self.rast = rast
        QtWidgets.QMainWindow.__init__(self)
        self.setMinimumSize(800,900)
        self.setMaximumSize(800,900)
        self.webView = QWebView()
        self.setCentralWidget(self.webView)
        self.setWindowTitle("Mesaj Önizleme")
        self.setWindowIcon(QtGui.QIcon(Icons["Standart"]))
        
        if(os.path.isfile("C:/WhatsMessageSender/WhatsAppGui/index_"+ str(self.rast) +".html")):
            self.webView.load(QtCore.QUrl.fromLocalFile("C:/WhatsMessageSender/WhatsAppGui/index_"+ str(self.rast) +".html"))
        else:
            self.webView.load(QtCore.QUrl.fromLocalFile(os.getcwd() + "/WhatsAppGui/index_"+ str(self.rast) +".html"))

    def closeEvent(self, event):
        try:
            os.remove(os.getcwd() + "\\WhatsAppGui\\fFrame.jpg")
        except FileNotFoundError:
            pass

        os.remove("WhatsAppGui\\index_"+ self.rast  +".html")