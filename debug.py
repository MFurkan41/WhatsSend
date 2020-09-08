from time import sleep as bekle
import os
from selenium import webdriver


browser = webdriver.Chrome(executable_path=os.getcwd()+"\\chromedriver.exe")
browser.get("https://web.whatsapp.com")

bekle(5)


for i in range(3):
    bekle(1)
    print(str(i+1)+". saniye")
browser.quit()
exit()

print("Eee Çıkmadı mı?")