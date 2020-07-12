from PIL import Image
from io import BytesIO
from win32api import GetSystemMetrics

def save_qr(browser):
    ScRate = GetSystemMetrics(0)/1920
    browser.maximize_window()
    element = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/canvas')
    location = element.location
    size = element.size
    png = browser.get_screenshot_as_png()
    im = Image.open(BytesIO(png)) 

    im = im.crop((location['x'] -20, location['y'] -20, location['x'] + size['width'] + 10, location['y'] + size['height'] + 20))
    im = im.resize((int(250*ScRate),int(250*ScRate)))
    im.save('qrcode.png') 