# Python Standart Library Imports
import sys
import os
from time import sleep as bekle

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Local Imports
    ## Functions
from includes.funcs.whatsqr import save_qr
from includes.funcs.getexcel import GetExcel
from includes.funcs.htmlrequest import *
from includes.funcs.parseText import parseVersion
    ## Forms
from includes.forms.mainForm import *
from includes.forms.updateForm import Ui_MainWindow as UpdateForm

# Other Necessary Imports
from passlib.hash import sha256_crypt
from requests.exceptions import ConnectionError
import urllib.parse
import urllib.request
import webbrowser

#web.whatsapp.com/send?phone=905326045779&text=DENEME

def warnMessage(title,iconType,text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setIcon(iconType)
    msg.setText(text)
    
    x = msg.exec_()

VERSION = "1.5"

image_path = os.getcwd() + "\\qrcode.png"

class WPApp(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window,VERSION)
        self.apiKey = None
        self.window = window
        self.c = False

        # Menu Button Settings
        self.actionDosya_A.triggered.connect(self.openFile)
        self.actionAyarla.triggered.connect(self.settings)
        self.actionKapat.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.actionUpdate.triggered.connect(self.update)

        # QPushButton Settings
        self.pushButton.clicked.connect(self.sendwp)
        self.pushButton_2.clicked.connect(self.create_table_view)

        # Create Table and Model
        self.dbModel()

        # Look for Update and Driver
        self.update("warn")
        self.getDriver()

        # Common Variables
        self._translate = QtCore.QCoreApplication.translate

    def getDriver(self):
        if (os.path.exists(os.getcwd()+"\\geckodriver.exe") == False):
            warnMessage("Gerekli sürücüler yüklenmemiş.",QMessageBox.Warning,"Programın çalışması için gerekli olan sürücüler bulunamadı. Yüklemek için devam ediniz.")
            self.driverWindow = QtWidgets.QMainWindow()
            self.ui = UpdateForm()
            self.ui.setupUi(self.driverWindow, "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip")
            self.driverWindow.show()

    def update(self,*warn):
        if self.controlVersion(list(warn)[0]) == True:
            the_url = 'https://github.com/MFurkan41/WhatsCompRepo/raw/master/{}/WhatsMessageSender{}.exe'.format(list(parseVersion(self.othVERSION))[-1],list(parseVersion(self.othVERSION))[-1])
            webbrowser.open(the_url)
            sys.exit()

    def controlVersion(self,*warn):
        self.othVERSION = requests.get("https://github.com/MFurkan41/WhatsCompRepo/raw/master/version.txt")
        self.othVERSION = self.othVERSION.text
        if(list(parseVersion(self.othVERSION))[-1] != VERSION):
            warnMessage("Uyarı!",QMessageBox.Information,"Program güncel değil.          \n\nKurulu versiyon : "+ str(VERSION) + "\nYeni versiyon : "+ list(parseVersion(self.othVERSION))[-1] + "\n\nGüncellemek için devam ediniz.")
            return True
        else:
            if(list(warn)[0] != "warn"):
                liste = parseVersion(self.othVERSION)[str(list(parseVersion(self.othVERSION))[-1])]
                warnMessage("Program Güncel!",QMessageBox.Information,"Program Güncel.\nProgramınız sürümü : " + self.version + "\nYenilikler aşağıda sıralanmıştır;\n\n"+ '\n'.join(str(item) for item in liste))
            return False

    def create_table_view(self):
        model = QtWidgets.QFileSystemModel()
        model.setRootPath( QtCore.QDir.currentPath())

    def pageScroll(self,row:int):
        column = 0
        index = self.tableView.model().index(row, column)
        self.tableView.scrollTo(index)

    # Open Setting Menu
    def settings(self):
        self.subWindow = QtWidgets.QMainWindow()
        if self.apiKey == None:
            try:
                open("apiKey.txt","x",encoding="utf-8")
            except FileExistsError:
                fileapi = open("apiKey.txt","r", encoding='utf-8')
                self.apiKey =  fileapi.readlines()
                fileapi.close()
            else:
                self.apiKey = [""]
        self.ui = Ui_OtherWindow(self.subWindow,self.model.rawHeaders,self.apiKey)
        self.ui.my_signal.connect(self.dbModel)
        self.ui.my_signal2.connect(self.setKey)
        self.subWindow.show()

    # Get ApiKey From 'Sub_Menu.py'
    def setKey(self,key=None):
        if(key == ""):
            self.apiKey = ""
            warnMessage("Uyarı",QMessageBox.Warning,"Lütfen anahtarınızı giriniz.")
            fileapi = open("apiKey.txt","w", encoding='utf-8')
            fileapi.write("")
            fileapi.close()
            self.settings()
        else:
            self.apiKey = key
            fileapi = open("apiKey.txt","w", encoding='utf-8')
            fileapi.write(str(self.apiKey))
            fileapi.close()
            self.apiKeyControl(self.apiKey)
    # Create QTableView Model and Set Header Automaticly From A .txt File
    def dbModel(self,headers=None):
        if headers is None:
            try:
                fileHeader = open("Loc_headers.txt","r", encoding='utf-8')
                self.headers =  [line.rstrip() for line in fileHeader]
                fileHeader.close()
            except FileNotFoundError:
                self.headers = ["İsim","Telefon No (Örn 9053xx..)","Mesaj Durumu"]
                fileHeader = open("Loc_headers.txt","w", encoding='utf-8')
                fileHeader.write('\n'.join(self.headers) + '\n')
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
    # Open a .xlsx file with PyQt5.QFileDialog
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
            warnMessage("Qr Kodu Okutunuz!",QMessageBox.Information,"Lütfen programın sağ altında çıkan QR kodu telefonunuzdan okutunuz. Kod için 'OK' tuşuna basınız.")

            QtGui.QGuiApplication.processEvents()

            rec = 1161
            while self.tableView.horizontalScrollBar().isVisible() == True:
                self.window.resize(rec,700)
                rec += 10
            QtGui.QGuiApplication.processEvents()

            options = Options()
            options.headless = True

            try:
                browser = webdriver.Firefox(options=options,executable_path=os.getcwd()+"\\geckodriver.exe")
            except WebDriverException:
                warnMessage("Uyarı",QMessageBox.Warning,"Programın çalışabilmesi için 'Firefox' tarayıcısını yüklemeniz gerekmekte. Yüklü ise programı yeniden başlatmalısınız.")
                webbrowser.open("https://download-installer.cdn.mozilla.net/pub/firefox/releases/77.0.1/win32/tr/Firefox%20Installer.exe")
                sys.exit()
            browser.get("https://web.whatsapp.com")
            bekle(5)
            save_qr(browser)
            self.refreshimage()
            QtGui.QGuiApplication.processEvents()
            bekle(10)

            fList = []
            self.mesaj = str(self.plain.toPlainText())
            for i in range(len(self.headers)):
                if "{" + str(i) + "}" in self.mesaj:
                    fList.append(i)
            
            for i in range(len(self.numaralar)):
                gen=1
                while True:
                    execM = "self.mesaj = self.mesaj.format("
                    for i in fList:
                        execM += "str(self.numaralar[i][" + str(i) + "]),"
                    execM = execM[:-1] + ")"
                    try:
                        exec(execM)
                    except IndexError:
                        warnMessage("Uyarı",QMessageBox.Warning,"Size verilen sürede QR kodu okutmadınız. Lütfen tekrar deneyiniz.")
                        self.label_6.setText(_translate("MainWindow", "<html><body><p style='text-align:center'>QR CODE</p></body></html>"))
                        return
                    url = "https://web.whatsapp.com/send?phone="
                    url += str(self.numaralar[i][1])
                    url += "&text="
                    url += urllib.parse.quote_plus(self.mesaj)
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
                    warnMessage("Uyarı",QMessageBox.Information,"Mesaj Hakkınız Kalmadı.")
                    self.pushButton.setText(self._translate("MainWindow", "Mesaj Hakkınız Kalmadı"))
                    self.pushButton.setEnabled(False)
                    break

            warnMessage("Uyarı",QMessageBox.Information,"Listedeki tüm mesajlar atıldı.")
            browser.close()

    def changeTableItem(self, x):
        self.dbModel()
        self.numaralar[x][-1] = "✅"
        self.CreateTable(self.numaralar)
           
    def CreateTable(self, fromlist):
        # Create or Refresh the QtTableView from 'fromlist' variable
        for i in range(len(fromlist)):
            execution = "self.model.addCustomer(Customer(("
            for a in range(len(self.headers)):
                execution += "fromlist["+str(i)+"]["+str(a)+"], "
            execution = execution[:-2] + ")))"
            exec(execution,{'self': self,'fromlist':fromlist,'Customer':Customer},{'self': self,'fromlist':fromlist,'Customer':Customer})
        QtGui.QGuiApplication.processEvents()

    def apiKeyControl(self,key):
        try:
            self.info = HtmlRequest(key, True)
        except ConnectionError:
            warnMessage("TEKNİK ARIZA",QMessageBox.Critical,"Programın birlikte çalıştığı sunucularda hata var. Lütfen 'Hakkında' kısmındaki mailden ulaşınız.")
            self.pushButton.setText(self._translate("MainWindow", "TEKNİK ARIZA (Code : 001)"))
            self.pushButton.setEnabled(False)
        try:
            if self.info["error_message"] == "no_auth_key":
                warnMessage("Geçersiz Anahtar!",QMessageBox.Warning,"Verilen anahtar geçersiz, kontrol edip tekrar deneyiniz.")
                self.settings()
                self.c = True
                return
        except:
            pass

        try:
            print(self.info)
        except AttributeError:
            self.spinBox_4.setValue(0)
        else:
            self.subWindow.close()
            self.spinBox_4.setValue(self.info['mcount'])
            if self.info["mcount"] == 0:
                warnMessage("Uyarı!",QMessageBox.Critical,"Hoşgeldiniz {},\nMalesef mesaj hakkınız kalmadı.".format(self.info["name"]))
                self.pushButton.setText(self._translate("MainWindow", "Mesaj Hakkınız Yok"))
                QtGui.QGuiApplication.processEvents()
                self.pushButton.setEnabled(False)
            else:
                self.pushButton.setText(self._translate("MainWindow", "Başlat"))
                QtGui.QGuiApplication.processEvents()
                self.pushButton.setEnabled(True)
                warnMessage("Hoşgeldiniz!",QMessageBox.Information,"Hoşgeldiniz {},\nKalan Mesaj Hakkınız : {}".format(self.info["name"],self.info["mcount"]))

# Start App
app = QtWidgets.QApplication(sys.argv)

app.setApplicationName("WP Auto Message Sender")
app.setApplicationVersion(VERSION)
MainWindow = QtWidgets.QMainWindow()

ui = WPApp(MainWindow)

MainWindow.show()
app.exec_()