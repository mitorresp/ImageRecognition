import cv2
import numpy as np
import checkGZ

BASE_IMG = "assets/img/"
BASE_TEMP = "assets/tmp/"

checkGZ.checkGameZone()
# read game image
img1 = cv2.imread(BASE_IMG + "savedimage1.png")
img2 = cv2.imread(BASE_IMG + "savedimage2.png")

# read invader image template
template = cv2.imread(BASE_IMG + "invader_03_transparent.png", cv2.IMREAD_UNCHANGED)
hh, ww = template.shape[:2]

# extract invader base image and alpha channel and make alpha 3 channels
base = template[:, :, 0:3]
alpha = template[:, :, 3]
alpha = cv2.merge([alpha, alpha, alpha])

# do masked template matching and save correlation image
correlation1 = cv2.matchTemplate(img1, base, cv2.TM_CCORR_NORMED, mask=alpha)
correlation2 = cv2.matchTemplate(img2, base, cv2.TM_CCORR_NORMED, mask=alpha)

# set threshold and get all matches
threshhold = 0.95
loc1 = np.where(correlation1 >= threshhold)
loc2 = np.where(correlation2 >= threshhold)

# draw matches
result1 = img1.copy()
for pt in zip(*loc1[::-1]):
    cv2.rectangle(result1, pt, (pt[0] + ww, pt[1] + hh), (0, 0, 255), 1)
    print(pt)
result2 = img2.copy()
for pt in zip(*loc2[::-1]):
    cv2.rectangle(result2, pt, (pt[0] + ww, pt[1] + hh), (0, 0, 255), 1)
    print(pt)

# save results
cv2.imwrite(BASE_TEMP + "invader_03_base.png", base)
cv2.imwrite(BASE_TEMP + "invader_03_alpha.png", alpha)
cv2.imwrite(BASE_TEMP + "game_invader_matches_1.jpg", result1)
cv2.imwrite(BASE_TEMP + "game_invader_matches_2.jpg", result2)

cv2.imshow("base", base)
cv2.imshow("alpha", alpha)
cv2.imshow("result1", result1)
cv2.imshow("result2", result2)
cv2.waitKey(0)
cv2.destroyAllWindows()
