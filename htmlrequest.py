import ast
import requests

BASE_URL = "myolal80.pythonanywhere.com"
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
