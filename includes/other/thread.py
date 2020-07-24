from guiLoop import guiLoop
from improvedSends import *
import os
from time import sleep as bekle

# Selenium Imports
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,WebDriverException,NoSuchElementException,ElementNotInteractableException, UnexpectedAlertPresentException

# Gui Imports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import urllib.parse
from includes.funcs.htmlrequest import *
from includes.funcs.warnmessage import warnMessage

@guiLoop
def wpsend(self):
    browser = webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe")
    browser.get("https://web.whatsapp.com")
    """
    bekle(5)
    save_qr(browser)
    self.refreshimage()
    QtGui.QGuiApplication.processEvents()
    bekle(10)
    """
    QtGui.QGuiApplication.processEvents()
    fList = []
    self.mesaj = str(self.plain.toPlainText())
    for i in range(len(self.headers)):
        if "{" + str(i) + "}" in self.mesaj:
            fList.append(i)
    
    for i in range(len(self.numaralar)):
        QtGui.QGuiApplication.processEvents()
        execM = "self.mesaj = self.mesaj.format("
        for i in fList:
            execM += "str(self.numaralar[i][" + str(i) + "]),"
        execM = execM[:-1] + ")"
        try:
            if(len(fList) != 0):
                exec(execM)

        except IndexError:
            warnMessage("Uyarı",QMessageBox.Warning,"Size verilen sürede QR kodu okutmadınız. Lütfen tekrar deneyiniz.")
            return
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
                clickButton(browser,"//*[@id='main']/footer/div[1]/div[3]/button")
            elif(j[0].split("/")[-1].split(".")[1] in self.imageList):
                url += "&text="
                bekle(1)
                browser.get(url)
                clickButton(browser,"//*[@id='main']/header/div[3]/div/div[2]/div")
                enterInput(browser,"//*[@id='main']/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input",j[0])
                clickButton(browser,"//*[@id='app']/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div")
            else:
                url += "&text="
                bekle(1)
                browser.get(url)
                clickButton(browser,"//*[@id='main']/header/div[3]/div/div[2]/div")
                enterInput(browser,"//*[@id='main']/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button/input",j[0])
                clickButton(browser,"//*[@id='app']/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div")
            bekle(1)

        self.spinBox_2.setValue(int(self.spinBox_2.text()) + 1)
        self.spinBox_3.setValue(int(self.spinBox_3.text()) - 1)
        res = HtmlRequest(self.apiKey, False)
        self.pageScroll(int(i+1))
        if(res["message"] != "no_message_count"):
            
            self.spinBox_4.setValue(res["mcount"])
            self.changeTableItem(i)
            QtGui.QGuiApplication.processEvents()
        else:
            warnMessage("Uyarı",QMessageBox.Information,"Mesaj Hakkınız Kalmadı.")
            self.pushButton.setText(self._translate("MainWindow", "Mesaj Hakkınız Kalmadı"))
            self.pushButton.setEnabled(False)
            break
        QtGui.QGuiApplication.processEvents()
    bekle(0.5)
    clickButton(browser,"//*[@id='side']/header/div[2]/div/span/div[3]/div")
    clickButton(browser,"//*[@id='side']/header/div[2]/div/span/div[3]/span/div/ul/li[6]/div")
    bekle(0.5)
    browser.close()
    warnMessage("Uyarı",QMessageBox.Information,"Listedeki tüm mesajlar atıldı.")
    QtGui.QGuiApplication.processEvents()