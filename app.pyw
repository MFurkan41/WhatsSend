# Python Standart Library Imports
import sys,os,logging,codecs,itertools,requests,ctypes,threading
from time import sleep as bekle
from random import randint,choice
from collections import defaultdict
from packaging import version
from multiprocessing import freeze_support

# Selenium Imports
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,WebDriverException,NoSuchElementException,ElementNotInteractableException, UnexpectedAlertPresentException

from PyQt5.QtCore import Qt, QCoreApplication, QDir
from PyQt5.QtGui import QIcon, QGuiApplication
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QFileSystemModel, QMainWindow, QFileDialog


from includes import *

from includes.appIcons import Icons

# Other Necessary Imports
from requests.exceptions import ConnectionError
import urllib.parse
import urllib.request
import webbrowser
from openpyxl import Workbook
from pynput.keyboard import Key, Controller, KeyCode
from re import match

#web.whatsapp.com/send?phone=905326045779&text=DENEME

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

# Version Info
# cmdkey /delete:LegacyGeneric:target=git:https://github.com
with open("D:/Project/WhatsSend/v.txt","r") as f:
    VERSION = f.read()

# Start Logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
# Stop Logging

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_random_string():
    sample_letters = '0123456789abcdefghijklmnopqrstuvwxyz';
    result_str = ''.join((choice(sample_letters) for i in range(10)))
    return result_str

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class WPApp(mainForm):
    def __init__(self, window):
        self.setupUi(window,VERSION)
        self.apiKey = None
        self.window = window
        self.c = False
        self.numaralar = []
        self.keyboard = Controller()

        # Menu Button Settings
        self.actionDosya_A.triggered.connect(lambda : self.openFile())
        self.actionAyarla.triggered.connect(self.settings)
        self.actionKapat.triggered.connect(sys.exit)
        self.actionUpdate.triggered.connect(self.update)
        self.actionFeedBack.triggered.connect(lambda : webbrowser.open("https://form.jotform.com/210061801846953"))

        # QPushButton Settings
        self.pushButton.clicked.connect(self.sendwp)
        self.pushButton_2.clicked.connect(self.previewMessage)
        self.pushButton_3.clicked.connect(self.getReport)
        self.pushButton_4.clicked.connect(self.stopBrowser)
        self.pushButton_5.clicked.connect(self.new_tab)
        self.pushButton_6.clicked.connect(self.delete_tab)
        self.pushButton_7.clicked.connect(self.openEmojiTab)
        self.pushButton_8.clicked.connect(lambda : (self.CreateTable([]),self.BarCalc(["total",0])))

        # Button Press Effect
        self.pushButton_5.pressed.connect(lambda : self.pushButton_5.setIcon(QIcon(Icons["Plus-Press"])))
        self.pushButton_5.released.connect(lambda : self.pushButton_5.setIcon(QIcon(Icons["Plus"])))
        self.pushButton_6.pressed.connect(lambda : self.pushButton_6.setIcon(QIcon(Icons["Minus-Press"])))
        self.pushButton_6.released.connect(lambda : self.pushButton_6.setIcon(QIcon(Icons["Minus"])))
        
        # Create Table and Model
        self.dbModel()

        # Look for Update and Driver
        self.update("warn")
        self.accept()

        # Drag&Drop Settings
        self.tableView.dragEnterEvent = self.dragEnterEvent
        self.tableView.dragMoveEvent = self.dragMoveEvent
        self.tableView.dropEvent = self.dropEvent

        # Common Variables
        self._translate = QCoreApplication.translate

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
 
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
 
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.openFile(file_path)
 
            event.accept()
        else:
            event.ignore()

    def openEmojiTab(self):
        self.keyboard.press(KeyCode.from_vk(0x5B))
        self.keyboard.press(KeyCode.from_vk(0xBE))
        self.keyboard.release(KeyCode.from_vk(0xBE))
        self.keyboard.release(KeyCode.from_vk(0x5B))
        self.plain_1.setFocus()
        return

    def new_tab(self):
        tCount = self.tab.count()
        if(tCount >= 20):
            warnMessage("Uyarı!",QMessageBox.Warning,"Maksimum 20 adet mesaj kutucuğu oluşturabilirsiniz.")
            return
        code = "self.plain_" + str(tCount+1) + " = QPlainTextEdit(self.centralwidget);" + \
               "self.plain_" + str(tCount+1) + ".setPlaceholderText('Mesajınız...');" + \
               "self.tab.addTab(self.plain_" + str(tCount+1) + ", 'Mesaj " + str(tCount+1) + "')"
        exec(code)
        if(tCount > 2):
            for i in range(tCount+1):
                self.tab.setTabText(i, "M" + str(i+1))

    def delete_tab(self):
        tCount = self.tab.count()
        if(tCount != 1):
            self.tab.removeTab(tCount-1)
        if(self.tab.count() <= 3):
            for i in range(self.tab.count()):
                self.tab.setTabText(i, "Mesaj " + str(i+1))

    def accept(self):  
        if getTxtInfo()["accept"] == False:
            self.acceptwindow = QMainWindow()
            self.ui = acceptForm()
            self.ui.setupUi(self.acceptwindow)
            self.ui.buttonSignal.connect(self.controlAccept)
            self.acceptwindow.show()
        elif getTxtInfo()["accept"] == True:
            if eval(getTxtInfo()["splashOnStart"]):
                self.sp = QMainWindow()
                self.ui = splashForm()
                self.ui.setupUi(self.sp)
                self.ui.closeSignal.connect(lambda : self.openWindow(True))
                self.sp.show()
            else:
                self.openWindow(False)

    def openWindow(self,splash):
        if splash:
            self.sp.hide()
        self.window.show()
        self.getDriver()
    
    def controlAccept(self,val):
        if val == True:
            saveTxtInfo("accept",True)
            self.acceptwindow.close()
            self.window.show()
            self.getDriver()

    def stopBrowser(self):
        try:
            self.browser.quit()
        except Exception as e:
            print(e)
        self.pushButton_4.setVisible(False)

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
            if(name != ""):
                book = Workbook()
                sheet = book.active

                for idx ,row in enumerate(self.numaralar, 1):
                    row[1] = str(("$" + str(row[1]))[1:])
                    sheet.append(row)
                    sheet.cell(idx, 2).number_format = "$"
                try:
                    book.save(name[0])
                except:
                    return
                msgbox = QMessageBox()
                msgbox.setWindowModality(Qt.NonModal)
                msgbox.setWindowIcon(QIcon(Icons["Standart"]))
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setText("Raporunuz aşağıda belirtilen dosya yoluna kaydedilmiştir;\n"+ name[0] +"\n\n" + "Dosyayı açmak ister misiniz?\n")
                ac = msgbox.addButton('Evet', msgbox.ActionRole)
                ac.clicked.connect(lambda : os.startfile(name[0]))
                msgbox.addButton('Hayır', msgbox.ActionRole)
                
                msgbox.exec_()
        else:
            warnMessage("Uyarı!",QMessageBox.Warning,"Listedeki numaraların raporunu çıkartabilmek için mesaj atmanız gerekmektedir.")

    def previewMessage(self):
        if(not os.path.exists(os.getcwd()+"\\WhatsAppGui")):
            warnMessage("Gerekli sürücüler yüklenmemiş.",QMessageBox.Warning,"Mesaj Önizlemek için Gerekli Dosyalar İndirilecek. Yüklemek için devam ediniz.")
            self.driverWindow = QMainWindow()
            self.ui = updateForm()
            self.ui.setupUi(self.driverWindow, "http://furkanyolal.com.tr/wpsend/previewGui/WhatsAppGui.zip")
            self.driverWindow.show()
            return

        emptyMes = []
        for i in range(self.tab.count()):
            exec("self.x = self.plain_" + str(i+1) + ".toPlainText() == ''")
            if(self.x):
                emptyMes.append(i+1)
        if(len(emptyMes) != 0):
            convertList = [str(element) for element in emptyMes]
            if(len(emptyMes) == 1):
                warnMessage("Uyarı",QMessageBox.Warning,"{} numaralı mesaj boşluğunu doldurunuz.".format(",".join(convertList)))
            else:
                warnMessage("Uyarı",QMessageBox.Warning,"{} numaralı mesaj boşluklarını doldurunuz.".format(",".join(convertList)))
            return

        r = self.randMes()
        if(not r == ""):
            self.message = r + "\n\nMSG:" + get_random_string()
        else:
            warnMessage("Uyarı!",QMessageBox.Warning,"Mesaj yazılmadığından önizlemesine bakamazsınız.")
            return

        self.imageList = ["tiff","pjp","pjpeg","jfif","tif","gif","svg","bmp","png","jpeg", \
                        "svgz","jpg","webp","ico","xbm","dib"]  
        self.videoList = ["mp4","m4v","3gpp","mov","avi"]

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
                for j in range(1,len(self.headers)+1):
                    if "{" + str(j) + "}" in self.message:
                        fList.append(j)
                if(len(fList) != 0):
                    try:
                        QGuiApplication.processEvents()
                        execM = "self.message = self.message.format("
                        for a in range(len(self.headers)):
                            execM += "str(self.numaralar[0][" + str(a-1) + "]),"
                        execM = execM[:-1] + ")"
                        try:
                            exec(execM)
                        except IndexError:
                            warnMessage("Uyarı!",QMessageBox.Warning,"'Mesaj Durumu' kolonundaki veriyi mesajınıza ekleyemezsiniz. Lütfen '{"+ str(max(fList)) + "}' değerini siliniz.")
                            return
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
                getFirstFrame(self.list_of_files[i-1][0],str(i))
                a = linkFile('image',os.getcwd() + "\\WhatsAppGui\\fFrame{}.jpg".format(str(i)))
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
            file.write(self.index_raw.replace("%2F","/").replace("%3A",":").replace("%5C","/"))
        
        self.view = WebViewBrowser(rast)
        self.view.setWindowModality(Qt.ApplicationModal)
        self.view.show()

    def getDriver(self):
        if(isChrome() == False):
            warnMessage("Uyarı",QMessageBox.Warning,"Programın çalışabilmesi için 'Google Chrome' tarayıcısını yüklemeniz gerekmekte. Yüklü ise programı yeniden başlatmalısınız.")
            webbrowser.open("https://www.google.com/intl/tr_tr/chrome/")
            sys.exit()
        elif(isCodec() == False):
            warnMessage("Uyarı",QMessageBox.Warning,"Programın çalışabilmesi için 'K-Lite Codec' programını yüklemeniz gerekmekte. Kurulum için devam ediniz. Yüklü ise programı yeniden başlatmalısınız.")
            webbrowser.open("https://files3.codecguide.com/K-Lite_Codec_Pack_1587_Basic.exe")
            sys.exit()
        else:
            url = "https://www.googleapis.com/storage/v1/b/chromedriver/o/LATEST_RELEASE"
            resp = requests.get(url)
            latest_release = requests.get(resp.json()['mediaLink']).text
            try:
                installedVer = getTxtInfo()["driverVer"]
            except KeyError:
                os.remove(os.getcwd() + "\\info.txt")
                warnMessage("Uyarı!",QMessageBox.Information,"Bir hata oluştu, lütfen programı yeniden başlatınız.")
                sys.exit()

            if (latest_release != installedVer or installedVer == "0" or not os.path.exists(os.getcwd()+"\\chromedriver.exe")):
                warnMessage("Gerekli sürücüler yüklenmemiş.",QMessageBox.Warning,"Programın çalışması için gerekli olan sürücüler bulunamadı veya programın yeni sürümü yüklenmemiş. Yüklemek için devam ediniz.")
                self.driverWindow = QMainWindow()
                self.ui = updateForm()
                saveTxtInfo("driverVer",latest_release)
                self.ui.setupUi(self.driverWindow, "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(latest_release))
                self.driverWindow.show()
        
    def update(self,*warn):
        if self.controlVersion(list(warn)[0]) == True:
            the_url = 'https://github.com/MFurkan42/WhatsCompRepo/raw/master/{}/WhatsMessageSender{}.exe'.format(list(parseVersion(self.othVERSION))[-1],list(parseVersion(self.othVERSION))[-1])
            webbrowser.open(the_url)
            sys.exit()

    def controlVersion(self,*warn):
        try:
            self.othVERSION = requests.get("https://github.com/MFurkan42/WhatsCompRepo/raw/master/version.txt").text
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
        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())

    def pageScroll(self,row:int):
        column = 0
        index = self.tableView.model().index(row, column)
        self.tableView.scrollTo(index)

    def BarCalc(self,var):
        text = "{}/{} - {}%"
        if var[0] == "total":
            text = text.format("0",str(var[1]),"0")
            self.bar.setValue(0)
        elif var[0] == "sent":
            percent = round(100/len(self.numaralar)*int(var[1]),1)
            text = text.format(str(var[1]),str(len(self.numaralar)),str(percent))
            self.bar.setValue(percent)
        self.label.setText(text)

    # Open Setting Menu
    def settings(self):
        try:
            self.loading.close()
        except:
            pass
        self.subWindow = QMainWindow()
        if self.apiKey == None:
            self.apiKey = getTxtInfo()["key"]
        check = getTxtInfo()["splashOnStart"]
        self.ui = settingsForm(self.subWindow,self.model.rawHeaders,self.apiKey,check)
        self.ui.my_signal.connect(self.dbModel)
        self.ui.my_signal2.connect(self.setKey)
        self.subWindow.show()

    # Get ApiKey From 'Sub_Menu.py'
    def setKey(self,data=None):
        key, checkBox = data[0], data[1]
        if(key == ""):
            self.apiKey = ""
            warnMessage("Uyarı",QMessageBox.Warning,"Lütfen anahtarınızı giriniz.")
            saveTxtInfo("key","")
            self.settings()
        else:
            self.apiKey = key
            saveTxtInfo("key",str(self.apiKey))
            saveTxtInfo("splashOnStart",str(checkBox))

            self.loading = QMainWindow()
            self.ui = loadingForm()
            self.ui.setupUi(self.loading)
            self.loading.show()
            QGuiApplication.processEvents()

            self.apiKeyControl(self.apiKey,0)

    # Create QTableView Model and Set Header Automaticly From A .txt File
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
        QGuiApplication.processEvents()

    # Open a .xlsx file with PyQt5.QFileDialog
    def openFile(self, *fileName):
        if not fileName:
            fileName,_ = QFileDialog.getOpenFileName(self.window, "Excel Dosyası Aç", '', "Excel Dosyası (*.xlsx)")
        else:
            if len(fileName) > 1:
                warnMessage("Uyarı",QMessageBox.Warning,"Birden fazla dosyayı açamazsınız.")
                return
            fileName = str(fileName[0])
            if fileName.split(".")[-1] != "xlsx":
                warnMessage("Uyarı",QMessageBox.Warning,"Yanlış dosya formatı, dosyanız 'xlsx' formatında olmalıdır.")
                return
        if fileName:
            excel = GetExcel()
            excel.createList(fileName)
            self.dbModel()
            self.numaralar = excel.getList()
            if(len(self.numaralar[0]) == len(self.headers)):
                regEx = ["905","05","5"]
                wrongNumsIDs = []
                for dataID, numara in enumerate(self.numaralar):
                    numara = numara[1].replace(" ","").replace("(","").replace(")","").replace("+","")
                    for id,cont in enumerate(regEx):
                        if numara.startswith(cont):
                            nCont = id
                            break
                    if id == 0:
                        pass
                    elif id == 1:
                        numara = "9" + numara
                    elif id == 2:
                        numara = "90" + numara
                    else:
                        wrongNumsIDs.append(dataID+1)
                        
                    if len(numara) != 12:
                        wrongNumsIDs.append(dataID+1)
                    
                    self.numaralar[dataID][1] = numara

                bosluk = "\n"
                if len(wrongNumsIDs) != 0:
                    if len(wrongNumsIDs) >= 10:
                        bosluk = ", "
                    text = "Lütfen dosyanızda aşağıdaki satırları kontrol ediniz;\n"
                    for Id in wrongNumsIDs:
                        text += str(Id) + bosluk
                    warnMessage("Uyarı!",QMessageBox.Warning, text[:-2:])
                    return
                        

                for elem in self.numaralar:
                    elem[1] = str(elem[1])
                    elem[1].replace(' ','')[::]
                self.CreateTable(self.numaralar)
                self.BarCalc(["total",len(self.numaralar)])
            else:
                self.BarCalc(["total",0])
                warnMessage("Uyarı",QMessageBox.Warning,"Açmaya çalıştığınız dosyadaki kolon sayısı programdaki ile eşit değildir!")
    
    def sendwp(self):
        if(self.apiKey == "" or self.apiKey is None):
            if(getTxtInfo()["key"] == ""):
                warnMessage("Uyarı",QMessageBox.Warning,"Lütfen anahtarınızı giriniz.")
                self.settings()
            else:
                self.apiKey = getTxtInfo()["key"]
            return
        self.apiKeyControl(self.apiKey)

        if(len(self.numaralar) == 0):
            warnMessage("Uyarı",QMessageBox.Warning,"Hiç numara eklenmedi.")
            return
        
        emptyMes = []
        for i in range(self.tab.count()):
            exec("self.x = self.plain_" + str(i+1) + ".toPlainText() == ''")
            if(self.x):
                emptyMes.append(i+1)
        if(len(emptyMes) != 0):
            convertList = [str(element) for element in emptyMes]
            if(len(emptyMes) == 1):
                warnMessage("Uyarı",QMessageBox.Warning,"{} numaralı mesaj boşluğunu doldurunuz.".format(",".join(convertList)))
            else:
                warnMessage("Uyarı",QMessageBox.Warning,"{} numaralı mesaj boşluklarını doldurunuz.".format(",".join(convertList)))
            return

        self.apiKeyControl(self.apiKey)
        warnMessage("Qr Kodu Okutunuz!",QMessageBox.Information,"Lütfen QR kodu telefonunuzdan okutunuz. Kod için 'OK' tuşuna basınız.")

        rec = 1161*self.ScRate
        while self.tableView.horizontalScrollBar().isVisible() == True:
            self.window.resize(rec,700*self.ScRate)
            rec += 10*self.ScRate
        QGuiApplication.processEvents()
    
        _ = self.randMes()

        self.thread = MesThread(self.mesList,
                                self.numaralar,
                                self.list_of_files,
                                self.apiKey,
                                self.headers
                                )
        self.thread.start()
        self.thread.browserSignal.connect(self.BSignal)
        self.thread.pushButton_4.connect(lambda var: self.pushButton_4.setVisible(var))
        self.thread.spinBoxSignal.connect(self.spinBoxSignalFunc)
        self.thread.changeItemSignal.connect(lambda var: self.changeTableItem(var[0],var[1]))
        self.thread.pushButton.connect(lambda var: self.pushButton.setText(self._translate("MainWindow", "Mesaj Hakkınız Kalmadı")) if var==1 else(self.pushButton.setEnabled(False)))
        return

    def BSignal(self, browser):
        self.browser = browser

    def spinBoxSignalFunc(self,values):
        if(values[0] == 10):
            self.pageScroll(values[1])
        elif(values[0] == 4):
            self.spinBox_4.setValue(values[1])
        elif(values[0] == "done"):
            threading.Thread(target = self.stopBrowser).start()
            warnMessage("Uyarı",QMessageBox.Information,"Listedeki tüm mesajlar atıldı.")
            
        elif(values[0] == "2"):
            self.BarCalc(["sent",values[1]])

    def randMes(self):
        tCount = self.tab.count()
        mesList = []
        for i in range(tCount):
            code = "mesList.append(self.plain_" + str(i+1) + ".toPlainText())"
            exec(code)
        self.mesList = mesList
        return choice(mesList)

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
        self.tableView.reset()
        self.dbModel()
        if len(fromlist) == 0:
            self.numaralar = []
            QGuiApplication.processEvents()
            return
        for i in range(len(fromlist)):
            execution = "self.model.addCustomer(Customer(("
            for a in range(len(self.headers)):
                execution += "fromlist["+str(i)+"]["+str(a)+"], "
            execution = execution[:-2] + ")))"
            exec(execution,{'self': self,'fromlist':fromlist,'Customer':Customer},{'self': self,'fromlist':fromlist,'Customer':Customer})
        QGuiApplication.processEvents()

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
                    self.loading.close()
                    warnMessage("Uyarı!",QMessageBox.Critical,"Hoşgeldiniz {},\nMalesef mesaj hakkınız kalmadı.".format(self.info["name"]))
                    self.pushButton.setText(self._translate("MainWindow", "Mesaj Hakkınız Yok"))
                    QGuiApplication.processEvents()
                    self.pushButton.setEnabled(False)
                else:
                    self.loading.close()
                    self.pushButton.setText(self._translate("MainWindow", "Başlat"))
                    QGuiApplication.processEvents()
                    self.pushButton.setEnabled(True)
                    warnMessage("Hoşgeldiniz!",QMessageBox.Information,"Hoşgeldiniz {},\nKalan Mesaj Hakkınız : {}".format(self.info["name"],self.info["mcount"]))

# Start App
def StartApp():
    MainWindow = QMainWindow()
    m = WPApp(MainWindow)
    #MainWindow.show()
    return m

if __name__ == "__main__":
    if not is_admin():
        #freeze_support()
        import win32com.shell.shell as shell
        commands = 'powershell -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath "C:\WhatsMessageSender"'
        #shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
        
        # Icon Checker
        checkIcons()

        app = QApplication(sys.argv)

        app.setApplicationName("WP Auto Message Sender by Rapid")
        app.setApplicationVersion(VERSION)

        #app.setStyleSheet(open("style.qss","r").read())

        window = StartApp()
        
        sys.exit(app.exec_())
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

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