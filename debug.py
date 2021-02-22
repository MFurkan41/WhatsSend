from pynput.keyboard import Key, Controller
from time import sleep as bekle

keyboard = Controller()

bekle(2)
keyboard.press('a')
keyboard.release('a')