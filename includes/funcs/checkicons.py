from .appIcons import Icons
import os,requests,shutil
def checkIcons():
    for i in Icons.items():
        if(os.path.exists(i[1])):
            pass
        else:
            img = "http://furkanyolal.com.tr/wpsend/icons/" + i[1].split("\\")[-1]
            fileName = i[1].split("\\")[-1]

            respond = requests.get(img, stream = True)

            if(respond.status_code == 200):
                respond.raw.decode_content = True

                try:
                    with open(os.getcwd() + "\\includes\\icons\\" + fileName,"wb") as f:
                        shutil.copyfileobj(respond.raw, f)
                except FileNotFoundError:
                    try:
                        os.mkdir(os.getcwd() + "\\includes\\icons\\")
                    except:
                        os.mkdir(os.getcwd() + "\\includes\\")
                        os.mkdir(os.getcwd() + "\\includes\\icons\\")
                    
                    
                    
                    
                    