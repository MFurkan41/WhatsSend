from selenium import webdriver
from time import sleep as bekle
from selenium.webdriver.firefox.options import Options
import sys
from whatsqr import save_qr
from form import *
from getexcel import GetExcel
import os
from passlib.hash import sha256_crypt
from htmlrequest import *

#web.whatsapp.com/send?phone=905326045779&text=DENEME

image_path = os.getcwd() + "\\qrcode.png"

class WPApp(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.text= None
        self.actionDosya_A.triggered.connect(self.openFile)
        self.actionSettings.triggered.connect(self.openSecondDialog)
        self.actionKapat.triggered.connect(QtCore.QCoreApplication.instance().quit)
        #self.actionSettings.triggered.connect(exec("print('Merhaba')"))
        self.pushButton.clicked.connect(self.sendwp)

    def openFile(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(MainWindow,"Excel Dosyası Aç", "","Excel Files (*.xlsx)", options=options)
        if fileName:
            excel = GetExcel()
            excel.createList(fileName)
            self.numaralar = excel.getList()
            #print(self.numaralar)
            self.CreateTable(self.numaralar)
            self.spinBox.setValue(len(self.numaralar))
            self.spinBox_3.setValue(len(self.numaralar))
    def refreshimage(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setPixmap(QtGui.QPixmap("qrcode.png"))
    
    def sendwp(self):
        if(self.text is None):
                _translate = QtCore.QCoreApplication.translate
                self.pushButton.setText(_translate("MainWindow", "Lütfen Anahtarınızı Giriniz."))
                QtGui.QGuiApplication.processEvents()
                self.pushButton.setText(_translate("MainWindow", "Başlat"))
                bekle(2)  
                QtGui.QGuiApplication.processEvents()
                self.openSecondDialog()
        elif(self.spinBox.text() == "0"):
            _translate = QtCore.QCoreApplication.translate
            self.pushButton.setText(_translate("MainWindow", "Hiç numara eklenmemiş..."))
            QtGui.QGuiApplication.processEvents()
            self.pushButton.setText(_translate("MainWindow", "Başlat"))
            bekle(2)  
            QtGui.QGuiApplication.processEvents()
        else:
            _translate = QtCore.QCoreApplication.translate
            self.pushButton.setText(_translate("MainWindow", "Lütfen bekleyiniz..."))
            self.label_5.setText(_translate("MainWindow", "  MESAJINIZI YAZARKEN\n"
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
            #bekle(20)
            #browser.close()
            #browser.set_window_size(1, 1)
            QtGui.QGuiApplication.processEvents()
            bekle(10)
            for i in range(0,len(self.numaralar)):
                mesaj = str(self.lineEdit.text())
                mesaj = mesaj.format(self.numaralar[i][0])
                url = "https://web.whatsapp.com/send?phone="
                url += str(self.numaralar[i][1])
                url += "&text="
                url += mesaj
                browser.get(url)
                bekle(5)
                try:
                    browser.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
                except:
                    print("NO MESSAGE INPUT")
                    break
                    ### Pop-Up For No Message Input
                self.spinBox_2.setValue(int(self.spinBox_2.text()) + 1)
                self.spinBox_3.setValue(int(self.spinBox_3.text()) - 1)
                res = HtmlRequest(self.text,False)
                if(res["message"] != "no_message_count"):
                    
                    self.spinBox_4.setValue(res["mcount"])
                    self.changeTableItem(i)
                    QtGui.QGuiApplication.processEvents()
                else:
                    self.pushButton.setText(_translate("MainWindow", "Mesaj Hakkınız Kalmadı"))
                    QtGui.QGuiApplication.processEvents()
                    self.pushButton.setText(_translate("MainWindow", "Başlat"))
                    bekle(2)  
                    QtGui.QGuiApplication.processEvents()
                    break

            self.pushButton.setText(_translate("MainWindow", "İşlem Tamamlandı"))
            QtGui.QGuiApplication.processEvents()
            self.pushButton.setText(_translate("MainWindow", "Başlat"))
            bekle(2)  
            QtGui.QGuiApplication.processEvents()

            browser.close()

    def changeTableItem(self,x):
        self.numaralar[x][2] = "✅"
        self.CreateTable(self.numaralar)
           
    def CreateTable(self,fromlist):

        #Table Widget'a Yazdırma
        _translate = QtCore.QCoreApplication.translate
        self.tableWidget.setRowCount(len(fromlist))
        
        for i in range(len(fromlist)):
            # Vertical Header Create
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
            # Vertical Header Translate
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("MainWindow", str(i+1)))
                
            ### Settings
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)    

            # Items Create
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i, 2, item)
            # Items Translate
            item = self.tableWidget.item(i, 0)
            item.setText(_translate("MainWindow", fromlist[i][0]))
            item = self.tableWidget.item(i, 1)
            item.setText(_translate("MainWindow", fromlist[i][1]))
            item = self.tableWidget.item(i, 2)
            item.setText(_translate("MainWindow", fromlist[i][2]))

            ### Settings
            self.tableWidget.setSortingEnabled(__sortingEnabled)
    def openSecondDialog(self):
        self.text, okPressed = QtWidgets.QInputDialog.getText(MainWindow,"Api Key Control","Anahtarınız:", QtWidgets.QLineEdit.Normal, "")
        if okPressed and self.text != '':
            try:
                self.info = HtmlRequest(self.text,True)
            except SyntaxError:
                _translate = QtCore.QCoreApplication.translate
                self.pushButton.setText(_translate("MainWindow", "HATALI ANAHTAR"))
                QtGui.QGuiApplication.processEvents()
                self.pushButton.setText(_translate("MainWindow", "Başlat"))
                bekle(5)  
                QtGui.QGuiApplication.processEvents()
                self.openSecondDialog()
            self.spinBox_4.setValue(self.info["mcount"])
            if(self.info["mcount"] == 0):
                _translate = QtCore.QCoreApplication.translate
                self.pushButton.setText(_translate("MainWindow", "Mesaj Hakkınız Yok"))
                QtGui.QGuiApplication.processEvents()
                self.pushButton.setEnabled(False)

# Start App
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

ui = WPApp(MainWindow)

MainWindow.show()
app.exec_()