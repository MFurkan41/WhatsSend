import json,shutil,os

def getTxtInfo():
    while True:
        try:
            infotxt = open("info.txt","r", encoding='utf-8')
            info = ""
            for line in infotxt.readlines():
                info += (line.replace("\n",""))
            info = info.replace("\'", "\"")
            try:
                info = eval(info)
            except:
                raise FileNotFoundError
            infotxt.close()
            return info
        except FileNotFoundError:
            info = open("info.txt","w", encoding='utf-8')
            info.write("{'name':'','mail':'','key':'','headers':['İsim','Telefon No','Mesaj Durumu'],'accept':False,'driverVer':'0','splashOnStart':'True'}")
            info.close()
            continue
        else:
            break
            
def saveTxtInfo(component,newValue):
    while True:
        try:
            info = getTxtInfo()
            info[component] = newValue
            infotxt = open("info.txt","w",encoding="utf-8")
            infotxt.write(str(info))
        except FileNotFoundError:
            info = open("info.txt","w", encoding='utf-8')
            info.write("{'name':'','mail':'','key':'','headers':['İsim','Telefon No','Mesaj Durumu'],'accept':False,'driverVer':'0','splashOnStart':'True'}")
            info.close()
            continue
        else:
            break