from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

BASE_IMG = "assets/img/"
GAME_ZONE = [1400, 300, 650, 520]
SPEED_LIST = [0.5, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2]
points = 0
prev_shoots = []


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
        lookForImage("invader_04_transparent"),
        lookForImage("invader_03"),
        lookForImage("invader_02"),
        lookForImage("invader_01"),
    ]


def shootAt(box):
    global points, prev_shoots
    _continue = True

    for shot in prev_shoots[-3:]:
        calc = shot - ((box.left + int(box.width / 2)))
        if -5 >= calc <= 5:
            _continue = False
            print("calc", calc)

    if _continue:
        win32api.SetCursorPos(
            (box.left + int(box.width / 2), 50 + box.top + box.height)
        )
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        prev_shoots.append(box.left + int(box.width / 2))
        points += 5
        print(
            "\t\tShoted:" + str(box.left + int(box.width / 2)) + ", ",
            str(box.top + int(box.height / 2)),
            "  POINTS: ",
            points,
            prev_shoots,
        )
    if len(prev_shoots) > 5:
        prev_shoots = prev_shoots[-3:]


def stickman():
    while keyboard.is_pressed("q") == False:
        search = lookForInvaders()
        found = False

        idx = 5
        for x in search:
            if x != None:
                print(
                    (" invader 0" + str(idx) if idx <= 4 else " weapon ") + " -",
                    x,
                )
                time.sleep(0.01)
                shootAt(x)
                found = True
            idx -= 1

        global points
        if found:
            print("\n")
            print("speed " + str(int(points / 250)))
        time.sleep(SPEED_LIST[int(points / 250)])


if __name__ == "__main__":
    print("Good Night Miguel.\n")
    time.sleep(2)
    print("Ready and Waiting...\n")
    time.sleep(1)
    stickman()
    print("\nBye bye, Miguel.")
