from pyautogui import *
import pyautogui

BASE_IMG = "assets/img/"
GAME_ZONE = [1400, 300, 650, 520]


def checkGameZone():
    print(GAME_ZONE)
    im1 = pyautogui.screenshot(region=GAME_ZONE)
    im1.save(r"" + BASE_IMG + "savedimage.png")


checkGameZone()
