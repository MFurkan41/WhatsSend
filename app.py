# Python Standart Library Imports
import sys,os,logging,codecs,itertools,requests
from time import sleep as bekle
from random import randint
from collections import defaultdict
from packaging import version

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
from includes.funcs.txtinfo import getTxtInfo,saveTxtInfo
from includes.funcs.checkicons import checkIcons
from includes.funcs.getfirstframe import getFirstFrame
    ## Forms
from includes.forms.mainForm import *
from includes.forms.updateForm import Ui_MainWindow as UpdateForm
from includes.forms.subMenu import Ui_OtherWindow
    ## Other
from appIcons import Icons
from includes.other.thread import wpsend

# Other Necessary Imports
from requests.exceptions import ConnectionError
import urllib.parse
import urllib.request
from webview import create_window, start
import webbrowser
from openpyxl import Workbook

#web.whatsapp.com/send?phone=905326045779&text=DENEME

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

# Version Info
VERSION = "1.9"

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
        self.pushButton_3.clicked.connect(self.getReport)

        # Create Table and Model
        self.dbModel()

        # Look for Update and Driver
        self.update("warn")
        self.getDriver()

        # Common Variables
        self._translate = QtCore.QCoreApplication.translate

    def getReport(self):
        mesSent = False
        try:
            self.numaralar
        except:
            warnMessage("Uyarı!",QMessageBox.Warning,"Listede numara bulunmadığından rapor çıkartamazsınız.")
            return
        else:
            for numara in self.numaralar:
                if(numara[-1] != "❌"):
                    mesSent = True
        if(mesSent):
            name = QFileDialog.getSaveFileName(self.window, "Raporu Kaydet",filter="Excel Files (*.xlsx)")
            if(name):   
                book = Workbook()
                sheet = book.active

                for idx ,row in enumerate(self.numaralar, 1):
                    row[1] = str(("$" + str(row[1]))[1:])
                    sheet.append(row)
                    sheet.cell(idx, 2).number_format = "$"

                book.save(name[0])

                msgbox = QMessageBox()
                
                msgbox.setWindowModality(QtCore.Qt.NonModal)
                msgbox.setWindowIcon(QtGui.QIcon(Icons["Standart"]))
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setText("Raporunuz aşağıda belirtilen dosya yoluna kaydedilmiştir;\n"+ name[0] +"\n\n" + "Dosyayı açmak ister misiniz?\n")
                ac = msgbox.addButton('Evet', msgbox.ActionRole)
                ac.clicked.connect(lambda : os.startfile(name[0]))
                msgbox.addButton('Hayır', msgbox.ActionRole)
                # disconnect the clicked signal from the slots QMessageBox automatically sets
                msgbox.exec_()
        else:
            warnMessage("Uyarı!",QMessageBox.Warning,"Listedeki numaraların raporunu çıkartabilmek için mesaj atmanız gerekmektedir.")

    def previewMessage(self):
        if(not os.path.exists(os.getcwd()+"\\WhatsAppGui")):
            warnMessage("Gerekli sürücüler yüklenmemiş.",QMessageBox.Warning,"Mesaj Önizlemek için Gerekli Dosyalar İndirilecek. Yüklemek için devam ediniz.")
            self.driverWindow = QtWidgets.QMainWindow()
            self.ui = UpdateForm()
            self.ui.setupUi(self.driverWindow, "http://furkanyolal.com.tr/wpsend/previewGui/WhatsAppGui.zip")
            self.driverWindow.show()
            return
        self.message = str(self.plain.toPlainText())
        if(self.message != ""):
            self.imageList = ["tiff","pjp","pjpeg","jfif","tif","gif","svg","bmp","png","jpeg", \
                            "svgz","jpg","webp","ico","xbm","dib"]  
            self.videoList = ["mp4","m4v","3gpp","mov"]

            try:
                self.index
            except:
                with codecs.open(os.getcwd()+"\\WhatsAppGui\\index_raw.html","r","utf-8") as file:
                    self.index_raw = file.read()
                self.index = self.index_raw
            else:
                self.index_raw = self.index
         
            for i in range(1,len(self.list_of_files)+1):
                if(self.list_of_files[i-1][0] == "Mesaj"):
                    fList = []
                    for j in range(len(self.headers)):
                        if "{" + str(j) + "}" in self.message:
                            fList.append(j)
                    if(len(fList) != 0):
                        try:
                            QtGui.QGuiApplication.processEvents()
                            execM = "self.message = self.message.format("
                            for i in range(len(self.headers)):
                                execM += "str(self.numaralar[0][" + str(i) + "]),"
                            execM = execM[:-1] + ")"
                            exec(execM)
                        
                        except AttributeError:
                            warnMessage("Uyarı!",QMessageBox.Warning,"Listede numara bulunmadığından önizlemeyi bu şekilde yapamazsınız.")
                            return
                    
                    a = linkFile('message',str(self.message))
                    code = "self.index_raw = self.index_raw.replace('{file"+ str(i) +"}','"+ a +"')"
                    exec(code)
                elif(self.list_of_files[i-1][0].split(".")[-1] in self.imageList):
                    a = linkFile('image',self.list_of_files[i-1][0])
                    code = "self.index_raw = self.index_raw.replace('{file"+ str(i) +"}','"+ a +"')"
                    exec(code)
                elif(self.list_of_files[i-1][0].split(".")[-1] in self.videoList):
                    getFirstFrame(self.list_of_files[i-1][0])
                    a = linkFile('image',os.getcwd() + "\\WhatsAppGui\\fFrame.jpg")
                    code = "self.index_raw = self.index_raw.replace('{file"+ str(i) +"}','"+ a +"')"
                    exec(code)
                else:
                    a = linkFile('file',self.list_of_files[i-1][0])
                    code = "self.index_raw = self.index_raw.replace('{file"+ str(i) +"}','"+ a +"')"
                    exec(code)
                
            for i in range(1+len(self.list_of_files),26):
                self.index_raw = self.index_raw.replace("{file"+str(i)+"}","")
            
            rast = str(randint(1001,10000))

            with codecs.open(os.getcwd()+"\\WhatsAppGui\\index_"+ rast  +".html","w","utf-8") as file:
                file.write(self.index_raw)

            create_window("Mesaj Önizleme",url="WhatsAppGui\\index_"+ rast +".html",resizable=False,on_top=True,width=int(800*self.ScRate),height=int(750*self.ScRate))
            start()
            try:
                os.remove(os.getcwd() + "\\WhatsAppGui\\fFrame.jpg")
            except FileNotFoundError:
                pass

            os.remove("WhatsAppGui\\index_"+ rast  +".html")
        else:
            warnMessage("Uyarı!",QMessageBox.Warning,"Mesaj yazılmadığından önizlemesine bakamazsınız.")
        

    def getDriver(self):
        if (not os.path.exists(os.getcwd()+"\\chromedriver.exe")):
            warnMessage("Gerekli sürücüler yüklenmemiş.",QMessageBox.Warning,"Programın çalışması için gerekli olan sürücüler bulunamadı. Yüklemek için devam ediniz.")
            self.driverWindow = QtWidgets.QMainWindow()
            self.ui = UpdateForm()
            self.ui.setupUi(self.driverWindow, "https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_win32.zip")
            self.driverWindow.show()
        if(isChrome() == False):
            warnMessage("Uyarı",QMessageBox.Warning,"Programın çalışabilmesi için 'Google Chrome' tarayıcısını yüklemeniz gerekmekte. Yüklü ise programı yeniden başlatmalısınız.")
            webbrowser.open("https://www.google.com/intl/tr_tr/chrome/")
            sys.exit()

    def update(self,*warn):
        if self.controlVersion(list(warn)[0]) == True:
            the_url = 'https://github.com/MFurkan41/WhatsCompRepo/raw/master/{}/WhatsMessageSender{}.exe'.format(list(parseVersion(self.othVERSION))[-1],list(parseVersion(self.othVERSION))[-1])
            webbrowser.open(the_url)
            sys.exit()

    def controlVersion(self,*warn):
        try:
            self.othVERSION = requests.get("https://github.com/MFurkan41/WhatsCompRepo/raw/master/version.txt").text
        except ConnectionError:
            warnMessage("Uyarı!",QMessageBox.Warning,"Bilgisayarınız internete bağlı olmadığından bu programı kullanmazsınız.")
            sys.exit()

        LastVersion = version.parse(list(parseVersion(self.othVERSION))[-1])
        if(LastVersion > version.parse(VERSION)):
            warnMessage("Uyarı!",QMessageBox.Information,"Program güncel değil.          \n\nKurulu versiyon : "+ str(VERSION) + "\nYeni versiyon : "+ LastVersion.__str__() + "\n\nGüncellemek için devam ediniz.")
            return True
        elif(LastVersion < version.parse(VERSION)):
            warnMessage("Uyarı, Test Sürümü!",QMessageBox.Information,"Test Sürümü :" + VERSION + "\nGitHub'daki versiyon " + LastVersion.__str__())
        else:
            if(list(warn)[0] != "warn"):
                versionUpdates = parseVersion(self.othVERSION)[LastVersion.__str__()]
                warnMessage("Program Güncel!",QMessageBox.Information,"Program Güncel.\nProgramınız sürümü : " + self.version + "\nYenilikler aşağıda sıralanmıştır;\n\n"+ '\n'.join(str(item) for item in versionUpdates))
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
            self.apiKey = getTxtInfo()["key"]
        self.ui = Ui_OtherWindow(self.subWindow,self.model.rawHeaders,self.apiKey)
        self.ui.my_signal.connect(self.dbModel)
        self.ui.my_signal2.connect(self.setKey)
        self.subWindow.show()

    # Get ApiKey From 'Sub_Menu.py'
    def setKey(self,key=None):
        if(key == ""):
            self.apiKey = ""
            warnMessage("Uyarı",QMessageBox.Warning,"Lütfen anahtarınızı giriniz.")
            saveTxtInfo("key","")
            self.settings()
        else:
            self.apiKey = key
            saveTxtInfo("key",str(self.apiKey))
            self.apiKeyControl(self.apiKey,0)

    # Create QTableView Model and Set Header Automatically From A .txt File
    def dbModel(self,headers=None):
        if headers is None:
            self.headers = getTxtInfo()["headers"]
        else:
            saveTxtInfo("headers",headers)
            self.headers = headers
            
        self.headers.pop(self.headers.index("Mesaj Durumu"))
        self.headers.append("Mesaj Durumu")
        self.model = CustomerTableModel(self.headers)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        QtGui.QGuiApplication.processEvents()
    # Open a .xlsx file with PyQt5.QFileDialog
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.window, "Excel Dosyası Aç", '', "Excel Dosyası (*.xlsx)")
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
    
    def sendwp(self):
        if(self.apiKey == "" or self.apiKey is None):
            if(getTxtInfo()["key"] == ""):
                warnMessage("Uyarı",QMessageBox.Warning,"Lütfen anahtarınızı giriniz.")
                self.settings()
            else:
                self.apiKey = getTxtInfo()["key"]
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
            return
            

    def changeTableItem(self, x, kind):
        self.dbModel()
        if(kind == "tick"):
            self.numaralar[x][-1] = "✔️"
        elif(kind == "cross"):
            self.numaralar[x][-1] = "❌"
        elif(kind == "qMark"):
            self.numaralar[x][-1] = "❓"
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
            self.info
            saveTxtInfo("name",self.info["name"])
            saveTxtInfo("mail",self.info["email"])
        except AttributeError:
            self.spinBox_4.setValue(0)
        else:
            try:
                self.subWindow.close()
            except:
                pass
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
    # Icon Checker
    checkIcons()

    app = QtWidgets.QApplication(sys.argv)

    app.setApplicationName("WP Auto Message Sender")
    app.setApplicationVersion(VERSION)

    #app.setStyleSheet(open("style.qss","r").read())

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