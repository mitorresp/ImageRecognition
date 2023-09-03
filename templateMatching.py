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
    {"xValue": 10, "yValue": 10, "who": who[1]},
    {"xValue": 11, "yValue": 11, "who": who[3]},
    {"xValue": 12, "yValue": 12, "who": who[2]},
    {"xValue": 12, "yValue": 12, "who": who[2]},
    {"xValue": 12, "yValue": 12, "who": who[2]},
    {"xValue": 12, "yValue": 12, "who": who[2]},
    {"xValue": 12, "yValue": 12, "who": who[2]},
    {"xValue": 12, "yValue": 12, "who": who[2]},
]


def alreadyShoted(_x, _y, _idx):
    global prevShots

    for s in prevShots:
        if (
            who[_idx] == s["who"]
            and _x in range(s["xValue"] - 1, s["xValue"] + 1)
            and _y > (s["yValue"] + 30)
        ):
            print(" -> already SHOT: ", _x, _y, who[_idx])
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
            if not alreadyShoted(_x, _y, idx):
                cv2.rectangle(
                    _screen, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2
                )
                pyautogui.click(x=_x, y=_y)
                if not idx == 0:
                    points += 5
                found = True
                print(
                    f"\tSHOT!  Confident: {round(max_val, 3)}  Location: {_x,_y}  Who: {who[idx]}"
                )
                print("\tPoints: ", points)
                if points % 10 == 0:
                    text = ""
                    for s in prevShots:
                        text = (
                            text
                            + " { "
                            + str(s["xValue"])
                            + ", "
                            + str(s["yValue"])
                            + " "
                            + s["who"]
                            + " },"
                        )
                    print("\tPrevShots: ", text)

                cv2.imshow("Result", result)
                cv2.moveWindow("Result", 300, 40)
                cv2.imshow("Screen Shot", _screen)
                cv2.moveWindow("Screen Shot", 300, 380)
                cv2.waitKey(1)

            prevShots.pop(0)
            prevShots.append({"xValue": _x, "yValue": _y, "who": who[idx]})
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
