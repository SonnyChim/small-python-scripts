from mss.windows import MSS as mss
import numpy as np
import cv2 as cv
import time

with mss() as sct:
    monitor = (0,0,1920,1080)
    fps = [0,0,0,0,0,0,0,0,0,0]
    while True:
        last_time = time.perf_counter()
        img = np.array(sct.grab(monitor))
        fps.insert(0,1/(time.perf_counter()-last_time))
        fps.pop()
        print(np.average(fps),fps[0])
        cv.imshow("OpenCV/Numpy normal", img)
        if cv.waitKey(1) == ord("q"):
            break