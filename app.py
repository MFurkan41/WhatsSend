# Python Standart Library Imports
import sys,os,logging,codecs,itertools,requests
from time import sleep as bekle
from random import randint
from collections import defaultdict

# Selenium Imports
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,WebDriverException,NoSuchElementException,ElementNotInteractableException, UnexpectedAlertPresentException

# Local Imports
    ## Functions
from includes.funcs.whatsqr import save_qr
from includes.funcs.getexcel import GetExcel
from includes.funcs.htmlrequest import *
from includes.funcs.parseText import parseVersion
from includes.funcs.isChrome import isChrome
from includes.funcs.linkfile import linkFile
from includes.funcs.warnmessage import warnMessage
    ## Forms
from includes.forms.mainForm import *
from includes.forms.updateForm import Ui_MainWindow as UpdateForm
from includes.forms.subMenu import Ui_OtherWindow
    ## Other
from appIcons import Icons
from includes.other.thread import wpsend

# Other Necessary Imports
from passlib.hash import sha256_crypt
from requests.exceptions import ConnectionError
import urllib.parse
import urllib.request
import webview
import webbrowser

#web.whatsapp.com/send?phone=905326045779&text=DENEME

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

def warnMessage(title,iconType,text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setIcon(iconType)
    msg.setWindowIcon(QtGui.QIcon(Icons["Standart"]))
    msg.setText(text)
    
    x = msg.exec_()

# Version Info
VERSION = "1.7"

# Image Paths
image_path = os.getcwd() + "\\qrcode.png"

# Setup For Logging
logging.basicConfig(format='%(asctime)s - %(message)s',filename='wp.log',level=logging.DEBUG)
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
        self.pushButton_2.clicked.connect(self.previewMessage)

        # Create Table and Model
        self.dbModel()

        # Look for Update and Driver
        self.update("warn")
        self.getDriver()

        # Common Variables
        self._translate = QtCore.QCoreApplication.translate

    def previewMessage(self):
        message = str(self.plain.toPlainText())
        if(message != ""):
            with codecs.open(os.getcwd()+"\\WhatsAppGui\\index_raw.html","r","utf-8") as file:
                    self.index_raw = file.read()
            for i in range(1,len(self.list_of_files)+1):
                if(self.list_of_files[i-1][0] == "Mesaj"):
                    a = linkFile('message',message).replace("\n","").replace("\r","")
                    code = "self.index_raw = self.index_raw.format_map(SafeDict(file"+ str(i) +"='"+ a +"'))"
                    exec(code)
                else:
                    a = linkFile('file',self.list_of_files[i-1][0]).replace("\n","").replace("\r","")
                    code = "self.index_raw = self.index_raw.format_map(SafeDict(file"+ str(i) +"='"+ a +"'))"
                    exec(code)
                


            for i in range(1+len(self.list_of_files),26):
                self.index_raw = self.index_raw.replace("{file"+str(i)+"}","")
            
            rast = str(randint(1001,10000))

            with codecs.open(os.getcwd()+"\\WhatsAppGui\\index_"+ rast  +".html","w","utf-8") as file:
                file.write(self.index_raw)

            webview.create_window("Mesaj Önizleme","WhatsAppGui/index_"+ rast  +".html",resizable=False,on_top=True,width=int(800*self.ScRate),height=int(750*self.ScRate))
            webview.start()
            os.remove("WhatsAppGui\\index_"+ rast  +".html")

        else:
            warnMessage("Uyarı!",QMessageBox.Warning,"Mesaj yazılmadığından önizlemesine bakamazsınız.")

    def getDriver(self):
        if (os.path.exists(os.getcwd()+"\\chromedriver.exe") == False):
            warnMessage("Gerekli sürücüler yüklenmemiş.",QMessageBox.Warning,"Programın çalışması için gerekli olan sürücüler bulunamadı. Yüklemek için devam ediniz.")
            self.driverWindow = QtWidgets.QMainWindow()
            self.ui = UpdateForm()
            self.ui.setupUi(self.driverWindow, "https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_win32.zip")
            self.driverWindow.show()
        if(isChrome() == False):
            warnMessage("Uyarı",QMessageBox.Warning,"Programın çalışabilmesi için 'Chrome' tarayıcısını yüklemeniz gerekmekte. Yüklü ise programı yeniden başlatmalısınız.")
            webbrowser.open("https://www.google.com/intl/tr_tr/chrome/")
            sys.exit()


    def update(self,*warn):
        if self.controlVersion(list(warn)[0]) == True:
            the_url = 'https://github.com/MFurkan41/WhatsCompRepo/raw/master/{}/WhatsMessageSender{}.exe'.format(list(parseVersion(self.othVERSION))[-1],list(parseVersion(self.othVERSION))[-1])
            webbrowser.open(the_url)
            sys.exit()

    def controlVersion(self,*warn):
        try:
            self.othVERSION = requests.get("https://github.com/MFurkan41/WhatsCompRepo/raw/master/version.txt")
        except ConnectionError:
            warnMessage("Uyarı!",QMessageBox.Warning,"Bilgisayarınız internete bağlı olmadığından bu programı kullanmazsınız.")
            sys.exit()
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
            self.apiKeyControl(self.apiKey,0)
    # Create QTableView Model and Set Header Automatically From A .txt File
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
            
        self.headers.pop(self.headers.index("Mesaj Durumu"))
        self.headers.append("Mesaj Durumu")
        self.model = CustomerTableModel(self.headers)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        QtGui.QGuiApplication.processEvents()
    # Open a .xlsx file with PyQt5.QFileDialog
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.window, "Excel Dosyası Aç", os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Excel Dosyası (*.xlsx)")
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
            warnMessage("Qr Kodu Okutunuz!",QMessageBox.Information,"Lütfen QR kodu telefonunuzdan okutunuz. Kod için 'OK' tuşuna basınız.")

            rec = 1161*self.ScRate
            while self.tableView.horizontalScrollBar().isVisible() == True:
                self.window.resize(rec,700*self.ScRate)
                rec += 10*self.ScRate
            QtGui.QGuiApplication.processEvents()

            
            wpsend(self,self)
            

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

    def apiKeyControl(self,key,*control):
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
            try:
                control = control[0]
            except IndexError:
                pass
            if(control == 0):
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
def StartApp():
    MainWindow = QtWidgets.QMainWindow()
    m = WPApp(MainWindow)
    MainWindow.show()
    return m

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setApplicationName("WP Auto Message Sender")
    app.setApplicationVersion(VERSION)

    window = StartApp()
    app.exec_()

"""
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setApplicationName("WP Auto Message Sender")
    app.setApplicationVersion(VERSION)
    MainWindow = QtWidgets.QMainWindow()

    ui = WPApp(MainWindow)

    MainWindow.show()
    app.exec_()
"""