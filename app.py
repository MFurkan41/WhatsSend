# Python Standart Library Imports
import sys
import os
from time import sleep as bekle

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options

# Local Imports
from whatsqr import save_qr
from form import *
from getexcel import GetExcel
from htmlrequest import *
#from sub-menu import *

# Other Necessary Imports
from passlib.hash import sha256_crypt
from requests.exceptions import ConnectionError
import urllib.parse

#web.whatsapp.com/send?phone=905326045779&text=DENEME

def warnMessage(title,iconType,text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setIcon(iconType)
    msg.setText(text)
    x = msg.exec_()

image_path = os.getcwd() + "\\qrcode.png"

class WPApp(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.apiKey = None
        self.window = window

        # Menu Button Settings
        self.actionDosya_A.triggered.connect(self.openFile)
        self.actionAyarla.triggered.connect(self.settings)
        self.actionKapat.triggered.connect(QtCore.QCoreApplication.instance().quit)

        # QPushButton Settings
        self.pushButton.clicked.connect(self.sendwp)
        self.pushButton_2.clicked.connect(self.create_table_view)

        # Create Table and Model
        self.dbModel()

        # Common Variables
        self._translate = QtCore.QCoreApplication.translate

    def create_table_view(self):
        model = QtWidgets.QFileSystemModel()
        model.setRootPath( QtCore.QDir.currentPath())

    def pageScroll(self,row:int):
        column = 0
        index = self.tableView.model().index(row, column)
        self.tableView.scrollTo(index)

    def settings(self):
        self.window = QtWidgets.QMainWindow()
        if self.apiKey == None:
            fileapi = open("apiKey.txt","r", encoding='utf-8')
            self.apiKey =  fileapi.readlines()
            fileapi.close()
        self.ui = Ui_OtherWindow(self.window,self.model.rawHeaders,self.apiKey)
        self.ui.my_signal.connect(self.dbModel)
        self.ui.my_signal2.connect(self.setKey)
        self.window.show()

    def setKey(self,key=None):
        if(key is 0):
            print("\n-----------\nBoş\n-----------\n")
        else:
            self.apiKey = key
            fileapi = open("apiKey.txt","w", encoding='utf-8')
            fileapi.write(str(self.apiKey))
            fileapi.close()
            self.apiKeyControl(self.apiKey)

    def dbModel(self,headers=None):
        if headers is None:
            fileHeader = open("Loc_headers.txt","r", encoding='utf-8')
            self.headers =  [line.rstrip() for line in fileHeader]
            fileHeader.close()
        else:
            fileHeader = open("Loc_headers.txt","w", encoding='utf-8')
            fileHeader.write('\n'.join(headers) + '\n')
            fileHeader.close()
            self.headers = headers
        for i in range(len(self.headers)):
            if(self.headers[i] == "Mesaj Durumu"):
                m = i
        self.headers.pop(m)
        self.headers.append("Mesaj Durumu")
        self.model = CustomerTableModel(self.headers)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        QtGui.QGuiApplication.processEvents()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(MainWindow, "Excel Dosyası Aç", os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Excel Dosyası (*.xlsx)")
        if fileName:
            excel = GetExcel()
            excel.createList(fileName)
            self.dbModel()
            self.numaralar = excel.getList()
            if(len(self.numaralar[0]) == len(self.headers)):
                self.CreateTable(self.numaralar)
                self.spinBox.setValue(len(self.numaralar))
                self.spinBox_3.setValue(len(self.numaralar))
            else:
                self.spinBox.setValue(0)
                self.spinBox_3.setValue(0)
                warnMessage("Uyarı",QMessageBox.Warning,"Açmaya çalıştığınız dosyadaki kolon sayısı programdaki ile eşit değildir!")

    def refreshimage(self):
        self.label_6.setPixmap(QtGui.QPixmap("qrcode.png"))
        QtGui.QGuiApplication.processEvents()
    
    def sendwp(self):
        if(self.apiKey is None or self.apiKey == ""):
            warnMessage("Uyarı",QMessageBox.Warning,"Lütfen anahtarınızı giriniz.")
            self.settings()
        elif(self.spinBox.text() == "0"):
            self.apiKeyControl(self.apiKey)
            if(self.c == True):
                pass
            else:
                warnMessage("Uyarı",QMessageBox.Warning,"Hiç numara eklenmedi.")
        elif(self.plain.toPlainText() == ""):
            self.apiKeyControl(self.apiKey)
            warnMessage("Uyarı",QMessageBox.Warning,"Mesaj girilmedi.")
        else:
            self.apiKeyControl(self.apiKey)
            warnMessage("Qr Kodu Okutunuz!",QMessageBox.Information,"Lütfen programın sağ altında çıkan QR kodu telefonunuzdan okutunuz.")
            self.label_5.setText(self._translate("MainWindow", "  MESAJINIZI YAZARKEN\n"
    "  BUNA DİKKAT EDİNİZ.\n"
    "\n"
    "Eğer mesajın attığınız kişiye özel\n"
    " olması için isim kullanmak\n"
    " istiyorsanız, mesajınızda isim\n"
    " olmasını istediğiniz yere {}\n"
    " işaretlerini koyunuz.\n"
    "Aşağıdaki QR kodu telefonunuzdan okutunuz."))

            QtGui.QGuiApplication.processEvents()
            options = Options()
            options.headless = True
            browser = webdriver.Firefox(options=options,executable_path="C:\\Drivers\\geckodriver.exe")
            browser.get("https://web.whatsapp.com")
            bekle(5)
            save_qr(browser)
            self.refreshimage()
            QtGui.QGuiApplication.processEvents()
            bekle(10)
            for i in range(0, len(self.numaralar)):
                gen=1
                while True:
                    mesaj = str(self.plain.toPlainText())
                    mesaj = mesaj.format(self.numaralar[i][0])
                    url = "https://web.whatsapp.com/send?phone="
                    url += str(self.numaralar[i][1])
                    url += "&text="
                    url += urllib.parse.quote_plus(mesaj)
                    browser.get(url)

                    try:
                        bekle(gen*2+1)
                        button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/footer/div[1]/div[3]/button")))
                        button.click()
                    except (TimeoutException, ElementClickInterceptedException):
                        gen += 1
                        continue
                    break

                self.spinBox_2.setValue(int(self.spinBox_2.text()) + 1)
                self.spinBox_3.setValue(int(self.spinBox_3.text()) - 1)
                res = HtmlRequest(self.apiKey, False)
                self.pageScroll(i+1)
                if(res["message"] != "no_message_count"):
                    
                    self.spinBox_4.setValue(res["mcount"])
                    self.changeTableItem(i)
                    QtGui.QGuiApplication.processEvents()
                else:
                    self.pushButton.setText(self._translate("MainWindow", "Mesaj Hakkınız Kalmadı"))
                    QtGui.QGuiApplication.processEvents()
                    self.pushButton.setText(self._translate("MainWindow", "Başlat"))
                    bekle(2)  
                    QtGui.QGuiApplication.processEvents()
                    break

            self.pushButton.setText(self._translate("MainWindow", "İşlem Tamamlandı"))
            QtGui.QGuiApplication.processEvents()
            self.pushButton.setText(self._translate("MainWindow", "Başlat"))
            bekle(2)
            QtGui.QGuiApplication.processEvents()

            browser.close()

    def changeTableItem(self, x):
        self.dbModel()
        self.numaralar[x][2] = "✅"
        self.CreateTable(self.numaralar)
           
    def CreateTable(self, fromlist):
        # Create or Refresh the QtTableView from 'fromlist' variable
        for i in range(len(fromlist)):
            execution = "self.model.addCustomer(Customer(("
            for a in range(len(self.headers)):
                execution += "fromlist["+str(i)+"]["+str(a)+"], "
            execution = execution[:-2] + ")))"
            exec(execution,{'self': self,'fromlist':fromlist,'Customer':Customer},{'self': self,'fromlist':fromlist,'Customer':Customer})
            #model.addCustomer(Customer(fromlist[i][0], fromlist[i][1], fromlist[i][2]))
        QtGui.QGuiApplication.processEvents()

    def apiKeyControl(self,key):
        try:
            self.info = HtmlRequest(key, True)
        except SyntaxError:
            warnMessage("Geçersiz Anahtar!",QMessageBox.Warning,"Verilen anahtar geçersiz, kontrol edip tekrar deneyiniz.")
            self.settings()
            self.c = True
        except ConnectionError:
            warnMessage("TEKNİK ARIZA",QMessageBox.Critical,"Programın birlikte çalıştığı sunucularda hata var. Lütfen 'Hakkında' kısmındaki mailden ulaşınız.")
            self.pushButton.setText(self._translate("MainWindow", "TEKNİK ARIZA (Code : 001)"))
            self.pushButton.setEnabled(False) 
        try:
            print(self.info)
        except AttributeError:
            self.spinBox_4.setValue(0)
        else:
            self.spinBox_4.setValue(self.info['mcount'])
            if self.info["mcount"] == 0:
                warnMessage("Uyarı!",QMessageBox.Critical,"Mesaj hakkınız kalmadı.")
                self.pushButton.setText(self._translate("MainWindow", "Mesaj Hakkınız Yok"))
                QtGui.QGuiApplication.processEvents()
                self.pushButton.setEnabled(False)

# Start App
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

ui = WPApp(MainWindow)

MainWindow.show()
app.exec_()