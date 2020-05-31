import ast
import requests

BASE_URL = "127.0.0.1:5000"
def HtmlRequest(key,info):
    if(info == True):
        url = "http://" + BASE_URL + "/wp/_" + str(key) + "_"
        strdict = requests.get(url)
        a = ast.literal_eval(strdict.text)
        return a
    else:
        url = "http://" + BASE_URL + "/wp/" + str(key)
        strdict = requests.get(url)
        a = ast.literal_eval(strdict.text)
        return a
