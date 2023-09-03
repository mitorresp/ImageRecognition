import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui

pyautogui.PAUSE = 0

print("Press 'h' to start playing.")
print("Once started press 'q' to quit.")
keyboard.wait("h")
x = 1410
y = 240
sct = mss.mss()

BASE_IMG = "assets/img/"
BASE_TEMP = "assets/tmp/"
GAME_ZONE_1 = {"left": 1410, "top": 240, "width": 520, "height": 300}
THRESHOLD = 0.8

points = 0

weapon = cv2.imread(BASE_IMG + "weapon_00_transparent.png")
inv_01 = cv2.imread(BASE_IMG + "invader_01_transparent.png")
inv_02 = cv2.imread(BASE_IMG + "invader_02_transparent.png")
inv_03 = cv2.imread(BASE_IMG + "invader_03_transparent.png")
inv_04 = cv2.imread(BASE_IMG + "invader_04_transparent.png")
who = ["weapon", "inv_01", "inv_02", "inv_03", "inv_04"]
images_list = [weapon, inv_01, inv_02, inv_03, inv_04]

fps_time = time()
while True:
    idx = 0
    for img in images_list:
        screen = numpy.array(sct.grab(GAME_ZONE_1))

        # Cut off alpha
        screen_alpha_removed = screen[:, :, :3]

        result = cv2.matchTemplate(screen_alpha_removed, img, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        _screen = screen.copy()
        if max_val > 0.85:
            w = img.shape[1]
            h = img.shape[0]
            _x = GAME_ZONE_1["left"] + max_loc[0] + int(w / 2)
            _y = GAME_ZONE_1["top"] + max_loc[1] + int(h / 2)
            cv2.rectangle(
                _screen, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2
            )
            pyautogui.click(x=_x, y=_y)
            points += 5
            print(
                f"\tSHOT!  Confident: {round(max_val, 3)}  Location: {_x,_y}  Who: {who[idx]}"
            )

            cv2.imshow("Result", result)
            cv2.imshow("Screen Shot", _screen)
            cv2.waitKey(1)
            sleep(0.05)

        # cv2.destroyAllWindows()
        idx += 1
        if keyboard.is_pressed("q"):
            break
    sleep(0.10)
    if keyboard.is_pressed("q"):
        break
    print("FPS: {}".format(1 / (time() - fps_time)))
    fps_time = time()
