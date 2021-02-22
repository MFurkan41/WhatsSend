from guiLoop import guiLoop
import os
from time import sleep as bekle
from random import choice

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,WebDriverException,NoSuchElementException,ElementNotInteractableException, UnexpectedAlertPresentException, WebDriverException 

# Gui Imports
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QThread, pyqtSignal
import urllib.parse
from includes import *

def get_random_string():
    sample_letters = '0123456789abcdefghijklmnopqrstuvwxyz';
    result_str = ''.join((choice(sample_letters) for i in range(10)))
    return result_str

class MesThread(QThread):
    browserSignal = pyqtSignal(object)
    pushButton_4 = pyqtSignal(bool)
    pushButton = pyqtSignal(int)

    spinBoxSignal = pyqtSignal(list)
    changeItemSignal = pyqtSignal(list)

    def __init__(self,*args,parent=None):
        super(MesThread,self).__init__(parent)
        self.mesaj,self.numaralar,self.list_of_files,self.apiKey,self.headers = args

    def run(self):
        try:
            webdriver.DesiredCapabilities.CHROME["unexpectedAlertBehaviour"] = "accept"
            
            chrome_options = Options()
            chrome_options.add_argument("user-data-dir=" + os.getenv("LOCALAPPDATA") + "/Google/Chrome/User Data/Wp")
            browser = webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe",chrome_options = chrome_options)
            self.browserSignal.emit(browser)

            self.pushButton_4.emit(True)
            self.mesL = self.mesaj

            browser.get("https://web.whatsapp.com")

            QGuiApplication.processEvents()
            
            for i in range(len(self.numaralar)):
                QGuiApplication.processEvents()
                self.imageList = ["tiff","pjp","pjpeg","jfif","tif","gif","svg","bmp","png","jpeg", \
                                    "svgz","jpg","webp","ico","xbm","dib","m4v","mp4","3gpp","mov"]
                url = "https://web.whatsapp.com/send?phone="
                url += str(self.numaralar[i][1])
                #url += urllib.parse.quote_plus(self.mesaj)

                self.Rmesaj = choice(self.mesL)
                self.mesaj = self.Rmesaj + "\n\nMSG:" + get_random_string()

                fList = []
                for j in range(1,len(self.headers)):
                    if "{" + str(j) + "}" in self.mesaj:
                        self.mesaj = self.mesaj.replace("{" + str(j) + "}","{d"+ str(j) +"}")
                        fList.append(j)
                        
                if(len(fList) != 0):
                    execM = "self.mesaj = self.mesaj.format("
                    for x in fList:
                        execM += "d" + str(x) + " = str(self.numaralar[" + str(i) + "][" + str(x-1) + "]),"
                    execM = execM[:-1] + ")"
                    exec(execM)

                for j in self.list_of_files:
                    while True:
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
                        if(deger == 2):
                            continue
                        else:
                            break
                        bekle(1)

                #self.app.spinBox_2.setValue(int(self.spinBox_2.text()) + 1)
                self.spinBoxSignal.emit(["2",str(i+1)])
                res = HtmlRequest(self.apiKey, False)
                self.spinBoxSignal.emit([10,int(i+1)])
                if(res["error_message"] != "no_message_count"):
                    self.spinBoxSignal.emit([4,res["mcount"]])
                    if(deger == 0):
                        self.changeItemSignal.emit([i,"qMark"])
                    elif(deger == 1):
                        self.changeItemSignal.emit([i,"tick"])
                    QGuiApplication.processEvents()
                else:
                    warnMessage("Uyarı",QMessageBox.Information,"Mesaj Hakkınız Kalmadı.")
                    self.pushButton.emit(1)
                    self.pushButton.emit(0)
                    break
                QGuiApplication.processEvents()
            bekle(0.5)
            clickButton(browser,"//*[@id='side']/header/div[2]/div/span/div[3]/div")
            clickButton(browser,"//*[@id='side']/header/div[2]/div/span/div[3]/span/div/ul/li[7]/div")
            bekle(0.5)
            browser.quit()
            self.spinBoxSignal.emit(["done",0])
            QGuiApplication.processEvents()
            self.pushButton_4.emit(True)
        except WebDriverException:
            try:
                browser.quit()
            except:
                pass
            try:
                self.pushButton_4.emit(True)
            except:
                pass
        self.quit()

        
    