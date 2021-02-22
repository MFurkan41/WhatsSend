from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
import os
from includes import *
from ..appIcons import Icons


class WebViewBrowser(QMainWindow):
    def __init__(self,rast):
        self.rast = rast
        QMainWindow.__init__(self)
        self.setMinimumSize(800,900)
        self.setMaximumSize(800,900)
        self.webView = QWebView()
        self.setCentralWidget(self.webView)
        self.setWindowTitle("Mesaj Önizleme")
        self.setWindowIcon(QIcon(Icons["Standart"]))
        
        if(os.path.isfile("C:/WhatsMessageSender/WhatsAppGui/index_"+ str(self.rast) +".html")):
            self.webView.load(QUrl.fromLocalFile("C:/WhatsMessageSender/WhatsAppGui/index_"+ str(self.rast) +".html"))
        else:
            self.webView.load(QUrl.fromLocalFile(os.getcwd() + "/WhatsAppGui/index_"+ str(self.rast) +".html"))

    def closeEvent(self, event):
        for i in range(20):
            try:
                os.remove(os.getcwd() + "\\WhatsAppGui\\fFrame{}.jpg".format(i))
            except FileNotFoundError:
                pass

        os.remove("WhatsAppGui\\index_"+ self.rast  +".html")