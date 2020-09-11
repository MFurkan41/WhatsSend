from guiLoop import guiLoop
import os
from time import sleep as bekle

# Selenium Imports
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,WebDriverException,NoSuchElementException,ElementNotInteractableException, UnexpectedAlertPresentException, WebDriverException 

# Gui Imports
from PyQt5 import QtCore, QtGui, QtWidgets
import urllib.parse
from includes.funcs.htmlrequest import *
from includes.funcs.warnmessage import warnMessage,QMessageBox
from includes.funcs.improvedSends import clickButton,enterInput

#@guiLoop
class MesThread(QtCore.QThread):
    browserSignal = QtCore.pyqtSignal(object)
    pushButton_4 = QtCore.pyqtSignal(bool)
    pushButton = QtCore.pyqtSignal(int)

    spinBoxSignal = QtCore.pyqtSignal(list)
    changeItemSignal = QtCore.pyqtSignal(list)

    def __init__(self,*args,parent=None):
        super(MesThread,self).__init__(parent)
        self.mesaj,self.numaralar,self.list_of_files,self.apiKey,self.headers = args

    def run(self):
        try:
            webdriver.DesiredCapabilities.CHROME["unexpectedAlertBehaviour"] = "accept"
            browser = webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe")
            self.browserSignal.emit(browser)

            self.pushButton_4.emit(True)

            browser.get("https://web.whatsapp.com")
            
            """
            bekle(5)
            save_qr(browser)
            self.app.refreshimage()
            QtGui.QGuiApplication.processEvents()
            bekle(10)
            """

            QtGui.QGuiApplication.processEvents()
            fList = []
            for i in range(1,len(self.headers)):
                if "{" + str(i) + "}" in self.mesaj:
                    fList.append(i)
            
            for i in range(len(self.numaralar)):
                QtGui.QGuiApplication.processEvents()
                execM = "self.mesaj = self.mesaj.format("
                for i in fList:
                    execM += "str(self.numaralar[i][" + str(i-1) + "]),"
                execM = execM[:-1] + ")"
                if(len(fList) != 0):
                    exec(execM)
                self.imageList = ["tiff","pjp","pjpeg","jfif","tif","gif","svg","bmp","png","jpeg", \
                                    "svgz","jpg","webp","ico","xbm","dib","m4v","mp4","3gpp","mov"]
                url = "https://web.whatsapp.com/send?phone="
                url += str(self.numaralar[i][1])
                #url += urllib.parse.quote_plus(self.mesaj)
                
                for j in self.list_of_files:
                    if(j[0] == "Mesaj"):
                        url += "&text="
                        url += urllib.parse.quote_plus(self.mesaj)
                        bekle(1)
                        browser.get(url)
                        deger = clickButton(browser,"//*[@id='main']/footer/div[1]/div[3]/button")
                    elif(j[0].split("/")[-1].split(".")[1] in self.imageList):
                        url += "&text="
                        bekle(1)
                        browser.get(url)
                        deger = clickButton(browser,"//*[@id='main']/header/div[3]/div/div[2]/div")
                        enterInput(browser,"//*[@id='main']/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input",j[0])
                        clickButton(browser,"//*[@id='app']/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div")
                    else:
                        url += "&text="
                        bekle(1)
                        browser.get(url)
                        deger = clickButton(browser,"//*[@id='main']/header/div[3]/div/div[2]/div")
                        enterInput(browser,"//*[@id='main']/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button/input",j[0])
                        clickButton(browser,"//*[@id='app']/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div")
                    #res = HtmlRequest(self.app.apiKey, False)
                    bekle(1)

                #self.app.spinBox_2.setValue(int(self.spinBox_2.text()) + 1)
                self.spinBoxSignal.emit(["2","+1"])
                #self.app.spinBox_3.setValue(int(self.spinBox_3.text()) - 1)
                self.spinBoxSignal.emit(["3","-1"])
                res = HtmlRequest(self.apiKey, False)
                self.spinBoxSignal.emit([10,int(i+1)])
                if(res["message"] != "no_message_count"):
                    self.spinBoxSignal.emit([4,res["mcount"]])
                    if(deger == 0 ):
                        self.changeItemSignal.emit([i,"qMark"])
                    else:
                        self.changeItemSignal.emit([i,"tick"])
                    QtGui.QGuiApplication.processEvents()
                else:
                    warnMessage("Uyarı",QMessageBox.Information,"Mesaj Hakkınız Kalmadı.")
                    self.pushButton.emit(1)
                    self.pushButton.emit(0)
                    break
                QtGui.QGuiApplication.processEvents()
            bekle(0.5)
            clickButton(browser,"//*[@id='side']/header/div[2]/div/span/div[3]/div")
            clickButton(browser,"//*[@id='side']/header/div[2]/div/span/div[3]/span/div/ul/li[7]/div")
            bekle(0.5)
            browser.quit()
            self.spinBoxSignal.emit(["done",0])
            QtGui.QGuiApplication.processEvents()
            self.pushButton_4.emit(True)
        except WebDriverException:
            warnMessage("Uyarı!",QMessageBox.Warning,"Açılan 'komut istemi (cmd)' veya chrome sekmesi kapatıldı. Mesajların atılabilmesi için bu iki pencerenin açık olması gerekmektedir.")
        self.quit()

        
    