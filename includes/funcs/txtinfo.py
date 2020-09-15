import json

def getTxtInfo():
    while True:
        try:
            infotxt = open("info.txt","r", encoding='utf-8')
            info = ""
            for line in infotxt.readlines():
                info += (line.replace("\n",""))
            info = info.replace("\'", "\"")
            info = eval(info)
            infotxt.close()
            return info
        except FileNotFoundError:
            info = open("info.txt","w", encoding='utf-8')
            info.write("{'name':'','mail':'','key':'','headers':['İsim','Telefon No (Örn 9053xx..)','Mesaj Durumu'],'accept':False}")
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
            info.write("{'name':'','mail':'','key':'','headers':['İsim','Telefon No (Örn 9053xx..)','Mesaj Durumu'],'accept':False}")
            info.close()
            continue
        else:
            break