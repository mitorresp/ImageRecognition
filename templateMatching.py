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
GAME_ZONE_1 = {"left": 1420, "top": 340, "width": 500, "height": 350}
THRESHOLD = 0.75

points = 0

weapon = cv2.imread(BASE_IMG + "weapon_00_transparent.png")
inv_01 = cv2.imread(BASE_IMG + "invader_01_transparent.png")
inv_02 = cv2.imread(BASE_IMG + "invader_02_transparent.png")
inv_03 = cv2.imread(BASE_IMG + "invader_03_transparent.png")
inv_04 = cv2.imread(BASE_IMG + "invader_04_transparent.png")
images_list = [weapon, inv_01, inv_02, inv_03, inv_04]

who = ["weapon", "inv_01", "inv_02", "inv_03", "inv_04"]
prevShots = [
    {"value": 10, "who": who[1]},
    {"value": 11, "who": who[3]},
    {"value": 12, "who": who[2]},
]


def alreadyShoted(_x, _idx):
    global prevShots

    for s in prevShots:
        if who[_idx] == s["who"] and _x in range(s["value"] - 1, s["value"] + 1):
            print(" -> already SHOT", _x, who[_idx])
            return True

    return False


print("Playing...")
fps_time = time()
while True:
    idx = 0
    found = False

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
            if not alreadyShoted(_x, idx):
                cv2.rectangle(
                    _screen, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2
                )
                pyautogui.click(x=_x, y=_y)
                prevShots.pop(0)
                prevShots.append({"value": _x, "who": who[idx]})
                points += 5
                found = True
                print(
                    f"\tSHOT!  Confident: {round(max_val, 3)}  Location: {_x,_y}  Who: {who[idx]}"
                )
                print("\tPoints: ", points)
                # if points % 50 == 0:
                print("\tPrevShots: ", prevShots)

                cv2.imshow("Result", result)
                cv2.moveWindow("Result", 300, 40)
                cv2.imshow("Screen Shot", _screen)
                cv2.moveWindow("Screen Shot", 300, 380)
                cv2.waitKey(1)
            sleep(0.05)

        # cv2.destroyAllWindows()
        idx += 1
        if keyboard.is_pressed("q"):
            break
    sleep(0.10)
    if keyboard.is_pressed("q"):
        break
    if found:
        print("FPS: {}\n".format(round(1 / (time() - fps_time), 4)))
    fps_time = time()
