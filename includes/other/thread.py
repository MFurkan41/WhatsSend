from guiLoop import guiLoop
import os
from time import sleep as bekle

# Selenium Imports
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,WebDriverException,NoSuchElementException,ElementNotInteractableException, UnexpectedAlertPresentException

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
        url = "https://web.whatsapp.com/send?phone="
        url += str(self.numaralar[i][1])
        url += "&text="
        url += urllib.parse.quote_plus(self.mesaj)
        bekle(1)
        browser.get(url)
        while True:
            try:
                button = browser.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button")
                button.click()
            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException, UnexpectedAlertPresentException):
                bekle(0.5)
                QtGui.QGuiApplication.processEvents()
                continue
            else:
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
        QtGui.QGuiApplication.processEvents()

    warnMessage("Uyarı",QMessageBox.Information,"Listedeki tüm mesajlar atıldı.")
    browser.close()
    QtGui.QGuiApplication.processEvents()