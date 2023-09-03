from pyautogui import *
import pyautogui

BASE_IMG = "assets/img/"
GAME_ZONE_1 = [1410, 240, 520, 125]
GAME_ZONE_2 = [1410, 550, 520, 125]


def checkGameZone():
    print(GAME_ZONE_1)
    print(GAME_ZONE_2)
    im1 = pyautogui.screenshot(region=GAME_ZONE_1)
    im1.save(r"" + BASE_IMG + "savedimage1.png")
    im2 = pyautogui.screenshot(region=GAME_ZONE_2)
    im2.save(r"" + BASE_IMG + "savedimage2.png")


checkGameZone()
