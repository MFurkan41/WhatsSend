from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException,UnexpectedAlertPresentException
from time import sleep as bekle

def clickButton(browser,xpath):
    gen = 0
    while True:
        if(gen >= 5):
            try:
                browser.find_element_by_xpath("//*[@id='app']/div/span[2]/div/span/div/div/div/div/div/div[2]/div").click()
            except:
                pass
            else:
                return 0
            gen = 0
            continue
        try:
            browser.find_element_by_xpath(xpath).click()
        except (NoSuchElementException,ElementNotInteractableException, UnexpectedAlertPresentException):
            gen+=1
            bekle(0.5)
            continue
        else:
            break
    return 1

def enterInput(browser,xpath, key):
    while True:
        try:
            element = browser.find_element_by_xpath(xpath)
            if(element.get_attribute("type") != "file"):
                bekle(0.5)
                element.clear()
                bekle(0.5)
                element.clear()
                for i in key:
                    element.send_keys(i)
            else:
                element.send_keys(key)
        except (NoSuchElementException,ElementNotInteractableException):
            bekle(0.5)
            continue
        else:
            break    
