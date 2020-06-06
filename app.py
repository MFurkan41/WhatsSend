import sys
import os
from time import sleep as bekle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options

from whatsqr import save_qr
from form import *
from getexcel import GetExcel
from htmlrequest import *

from passlib.hash import sha256_crypt
from requests.exceptions import ConnectionError
import urllib.parse


#web.whatsapp.com/send?phone=905326045779&text=DENEME

image_path = os.getcwd() + "\\qrcode.png"


class WPApp(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.text= None

        # Menu Button Settings
        self.actionDosya_A.triggered.connect(self.openFile)
        self.actionAyarla.triggered.connect(self.openSecondDialog)
        self.actionKapat.triggered.connect(QtCore.QCoreApplication.instance().quit)

        # QPushButton Settings
        self.pushButton.clicked.connect(self.sendwp)
        self.pushButton_2.clicked.connect(self.setColumnWidth)

        # Create Table and Model
        self.dbModel()

        # Common Variables
        self._translate = QtCore.QCoreApplication.translate

    def setColumnWidth(self):
        ##self.tableView.setColumnWidth(0,150)
        pass

    def pageScroll(self,row:int):
        column = 0
        index = self.tableView.model().index(row, column)
        self.tableView.scrollTo(index)


    def dbModel(self):
        self.model = CustomerTableModel()
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(MainWindow, "Excel Dosyası Aç", os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Excel Dosyası (*.xlsx)")
        if fileName:
            excel = GetExcel()
            excel.createList(fileName)
            self.dbModel()
            self.numaralar = excel.getList()
            self.CreateTable(self.numaralar)
            self.spinBox.setValue(len(self.numaralar))
            self.spinBox_3.setValue(len(self.numaralar))
            
    def refreshimage(self):
        self.label_6.setPixmap(QtGui.QPixmap("qrcode.png"))
    
    def sendwp(self):
        if(self.text is None or self.text == ""):
            self.pushButton.setText(self._translate("MainWindow", "Lütfen Anahtarınızı Giriniz."))
            QtGui.QGuiApplication.processEvents()
            self.pushButton.setText(self._translate("MainWindow", "Başlat"))
            bekle(2)  
            QtGui.QGuiApplication.processEvents()
            try:
                self.openSecondDialog()
            except ConnectionError:
                self.pushButton.setText(self._translate("MainWindow", "TEKNİK ARIZA (Code : 001)"))
                self.pushButton.setEnabled(False)

        elif(self.spinBox.text() == "0"):
            self.pushButton.setText(self._translate("MainWindow", "Hiç numara eklenmemiş..."))
            QtGui.QGuiApplication.processEvents()
            self.pushButton.setText(self._translate("MainWindow", "Başlat"))
            bekle(2)  
            QtGui.QGuiApplication.processEvents()
        elif(self.plain.toPlainText() == ""):
            self.pushButton.setText(self._translate("MainWindow", "Lütfen mesaj giriniz."))
            QtGui.QGuiApplication.processEvents()
            self.pushButton.setText(self._translate("MainWindow", "Başlat"))
            bekle(2)  
            QtGui.QGuiApplication.processEvents()
        else:
            self.pushButton.setText(self._translate("MainWindow", "Lütfen bekleyiniz..."))
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
                res = HtmlRequest(self.text, False)
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
        for i in range(0, len(fromlist)):
            self.model.addCustomer(Customer(fromlist[i][0], fromlist[i][1], fromlist[i][2]))
        QtGui.QGuiApplication.processEvents()

    def openSecondDialog(self):
        self.text, okPressed = QtWidgets.QInputDialog.getText(MainWindow, "Api Key Control", "Anahtarınız:", QtWidgets.QLineEdit.Normal, "")
        if okPressed and self.text != '':
            try:
                self.info = HtmlRequest(self.text, True)
            except SyntaxError:
                self.pushButton.setText(self._translate("MainWindow", "HATALI ANAHTAR"))
                QtGui.QGuiApplication.processEvents()
                self.pushButton.setText(self._translate("MainWindow", "Başlat"))
                bekle(5)  
                QtGui.QGuiApplication.processEvents()
                self.openSecondDialog()
            except ConnectionError:
                self.pushButton.setText(self._translate("MainWindow", "TEKNİK ARIZA (Code : 001)"))
                self.pushButton.setEnabled(False) 
            try:
                print(self.info)
            except AttributeError:
                self.spinBox_4.setValue(0)
            else:
                self.spinBox_4.setValue(self.info['mcount'])
                if self.info["mcount"] == 0:
                    self.pushButton.setText(self._translate("MainWindow", "Mesaj Hakkınız Yok"))
                    QtGui.QGuiApplication.processEvents()
                    self.pushButton.setEnabled(False)

# Start App
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

ui = WPApp(MainWindow)

MainWindow.show()
app.exec_()