import numpy as np
import cv2 as cv
import pyautogui as pa

img = pa.screenshot()
img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
cv.namedWindow("screen",cv.WINDOW_NORMAL)
cv.setWindowProperty("screen",cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
cv.imshow("screen",img)
breakanim = []
for i in range(10):
    breakanim.append(cv.imread(f"block breaking animation/destroy_stage_{i}.png"))
    breakanim[i] = cv.resize(breakanim[i],(1920,1080),None,0,0,cv.INTER_NEAREST)

cv.waitKey()
for i in range(10):
    cv.imshow("screen",cv.multiply(img,breakanim[i]/255,dtype=0))
    cv.waitKey()
pa.hotkey("winleft","d")
