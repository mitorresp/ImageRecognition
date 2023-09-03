from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

BASE_IMG = "assets/img/"
GAME_ZONE = [1400, 300, 650, 520]
SPEED_LIST = [1, 0.7, 0.5, 0, 3]
points = 0


def lookForImage(imgName):
    return pyautogui.locateOnScreen(
        BASE_IMG + imgName + ".png",
        region=GAME_ZONE,
        grayscale=True,
        confidence=0.8,
    )


def lookForInvaders():
    return [
        lookForImage("weapon_transparent"),
        lookForImage("invader_01"),
        lookForImage("invader_02"),
        lookForImage("invader_03"),
        lookForImage("invader_04_transparent"),
    ]


def shootAt(box):
    win32api.SetCursorPos((box.left + int(box.width / 2), 50 + box.top + box.height))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    points = points + 5
    print(
        "\t\tShoted:" + str(box.left + int(box.width / 2)) + ", ",
        str(box.top + int(box.height / 2)),
        "  POINTS: ",
        points,
    )


def stickman():
    while keyboard.is_pressed("q") == False:
        search = lookForInvaders()
        found = False

        idx = 0
        for x in search:
            if x != None:
                print(
                    (" invader 0" + str(idx) if idx >= 1 else " weapon ") + " -",
                    x,
                )
                time.sleep(0.01)
                shootAt(x)
                found = True
            idx += 1

        if found:
            print("\n")
        time.sleep(SPEED_LIST[0])


if __name__ == "__main__":
    print("Good Night Miguel.\n")
    time.sleep(2)
    print("Starting\n")
    time.sleep(1)
    stickman()
    print("\nBye bye, Miguel.")
