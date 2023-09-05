from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

BASE_IMG = "assets/img/"
GAME_ZONE_1 = [1410, 240, 520, 200]
GAME_ZONE_2 = [1410, 550, 520, 200]
SPEED_LIST = [0.6, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2]
points = 0


def lookForImage(imgName, gameZone):
    return pyautogui.locateOnScreen(
        BASE_IMG + imgName + ".png",
        region=gameZone,
        grayscale=False,
        confidence=0.70,
    )


def lookForInvaders():
    return [
        lookForImage("weapon_transparent", GAME_ZONE_2),
        lookForImage("invader_04_transparent", GAME_ZONE_2),
        lookForImage("invader_03_transparent", GAME_ZONE_2),
        lookForImage("invader_02_transparent", GAME_ZONE_2),
        lookForImage("invader_01_transparent", GAME_ZONE_2),
        lookForImage("weapon_transparent", GAME_ZONE_1),
        lookForImage("invader_04_transparent", GAME_ZONE_1),
        lookForImage("invader_03_transparent", GAME_ZONE_1),
        lookForImage("invader_02_transparent", GAME_ZONE_1),
        lookForImage("invader_01_transparent", GAME_ZONE_1),
    ]


def shootAt(box):
    global points
    win32api.SetCursorPos((box.left + int(box.width / 2), 50 + box.top + box.height))
    time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    print(
        "\t\tShoted:" + str(box.left + int(box.width / 2)) + ", ",
        str(box.top + int(box.height / 2)),
        "  POINTS: ",
        points,
    )


def stickman():
    global points
    while keyboard.is_pressed("q") == False:
        search = lookForInvaders()
        found = False

        idx = 10
        for x in search:
            if x != None:
                if idx == 5 or idx == 10:
                    print(
                        " weapon  -",
                        x,
                    )
                else:
                    print(
                        " invader 0" + str(idx) + " -",
                        x,
                    )
                    points += 5

                time.sleep(0.01)
                shootAt(x)
                found = True

            idx -= 1

        if found:
            print("\n")
            # print("speed " + str(int(points / 250)))
        time.sleep(SPEED_LIST[int(points / 250)])


if __name__ == "__main__":
    print("Good Night Miguel.\n")
    time.sleep(2)
    print("Ready and Waiting...\n")
    time.sleep(1)
    stickman()
    print("\nBye bye, Miguel.")
