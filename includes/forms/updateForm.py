# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox, QWidget, QProgressBar, QLabel, QMenuBar, QStatusBar
from PyQt5.QtCore import QRect, QSize, Qt, QMetaObject, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import sys
import os
from win32api import GetSystemMetrics
from includes import *
from ..appIcons import Icons

import queue
import requests
import zipfile


def warnMessage(title,iconType,text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setIcon(iconType)
    msg.setWindowIcon(QIcon(Icons["Standart"]))
    msg.setText(text)
    
    x = msg.exec_()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, url):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(576, 117)

        MainWindow.setWindowFlags(MainWindow.windowFlags() | Qt.WindowStaysOnTopHint)
        MainWindow.setWindowIcon(QIcon(Icons["Download"]))

        self.MainWindow = MainWindow
        self.url = url

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QProgressBar(self.centralwidget,minimumWidth=400)
        self.progressBar.setGeometry(QRect(30, 50, 531, 31))
        self.progressBar.setMinimumSize(QSize(531, 31))
        self.progressBar.setMaximumSize(QSize(531, 31))
        self.progressBar.setValue(0)
        self.progressBar.setObjectName("progressBar")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(10, 20, 250, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 576, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        self.on_pushButton_clicked()

        # Download button event
    def on_pushButton_clicked(self):
        the_url = self.url
        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        self.the_filepath = os.getcwd() + "\\" +self.url.split(chr(47))[-1]
        the_fileobj = open(self.the_filepath, 'wb')
        #### Create a download thread
        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()

    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            try:
                os.remove("\\".join(self.the_filepath.split("\\")[:-1]) + "\\chromedriver.exe")
            except FileNotFoundError:
                pass
            with zipfile.ZipFile(self.the_filepath, 'r') as zip_ref:
                zip_ref.extractall(os.getcwd()+"\\")
            self.MainWindow.close()
            os.remove(self.the_filepath)
            warnMessage("Bilgi",QMessageBox.Information,"Gerekli dosyalar yüklendi, programı kullanabilirsiniz.")
            


    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wp Auto Message Sender - Sürücü"))
        self.label.setText(_translate("MainWindow",  "Gerekli sürücüler indiriliyor..."))

class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)                        #Create signal

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer


    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)                #Streaming download mode
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)                            #Setting Pointer Position
                self.fileobj.write(chunk)                            #write file
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))        #Sending signal
            #######################################################################
            self.fileobj.close()    #Close file
            self.exit(0)            #Close thread


        except Exception as e:
            print(e)
