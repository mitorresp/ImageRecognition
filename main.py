from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

BASE_IMG = "assets/img/"


def stickman():
    while 1:
        if (
            pyautogui.locateOnScreen(
                BASE_IMG + "stickman.png",
                region=(1450, 100, 400, 400),
                grayscale=True,
                confidence=0.8,
            )
            != None
        ):
            print("I can see it")
            time.sleep(0.5)
        else:
            print("I am unable to see it")
            time.sleep(0.5)


if __name__ == "__main__":
    print("Good Night Miguel.")
    stickman()
    print("Bye bye, Miguel.")
