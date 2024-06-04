from mss.windows import MSS as mss
import numpy as np
import cv2 as cv
from pynput import keyboard
from pynput.mouse import Controller,Button
import time

def on_press(key):
    global running,listening,setwindow
    if key == keyboard.Key.esc:
        listening = False
        return False
    if key == keyboard.Key.f8:
        running = not running
    if key == keyboard.Key.f9:
        setwindow = True

def mouseinput(event,x,y,flags,param):
    global drawcoords,drawing,x1,y1
    if drawing:
        if event == cv.EVENT_LBUTTONDOWN:
            x1 = np.abs(x)
            y1 = np.abs(y)
        if event == cv.EVENT_LBUTTONUP:
            drawcoords = (np.minimum(x1,np.maximum(x,0)),np.maximum(x1,np.maximum(x,0)),np.minimum(y1,np.maximum(y,0)),np.maximum(y1,np.maximum(y,0)))
            drawing = False



with keyboard.Listener(on_press=on_press) as listener:
    running = False
    listening = True
    setwindow = False
    mouse = Controller()
    rng = np.random.default_rng()
    with mss() as sct:
        frametime = time.perf_counter()
        while listening:
            if setwindow:
                fullimg = np.array(sct.grab((0,0,1920,1080)))
                cv.namedWindow("draw",cv.WINDOW_NORMAL)
                cv.setWindowProperty("draw",cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
                cv.imshow("draw",fullimg)
                cv.setMouseCallback("draw", mouseinput)
                drawing = True
                while drawing:
                    if cv.waitKey(1) == ord("q"):
                        raise SystemExit
                cv.destroyWindow("draw")
                monitor = (int(drawcoords[0]),int(drawcoords[2]),int(drawcoords[1]),int(drawcoords[3]))
                setwindow = False
            if running and time.perf_counter() > frametime + 0.1:
                frametime = time.perf_counter()
            # if running:
                img = np.array(sct.grab(monitor))
                coordinates = np.argwhere(img[:,:,2]>img[:,:,0])
                # coordinates = np.argwhere(img[:,:,2]>128)
                # mouse.position = (coordinates[0][1]+monitor[0],coordinates[0][0]+monitor[1])
                # mouse.press(Button.left)
                # mouse.release(Button.left)
                targets = np.array([[-100,-100]])
                for value in coordinates:
                    target_found = True
                    for i in targets:
                        if abs(i[0]-value[0]) < 10 or abs(i[1]-value[1]) < 10:
                            target_found = False
                            break
                    if target_found:
                        targets = np.append(targets,[value],0)
                targets = np.delete(targets,0,0)
                for value in targets:
                    mouse.position = (value[1]+monitor[0],value[0]+monitor[1])
                    mouse.press(Button.left)
                    mouse.release(Button.left)


                # pixels = coordinates.shape[0]
                # for i in range(np.min((pixels//100,5))):
                #     coordinate = coordinates[rng.integers(pixels),0:2]
                #     mouse.position = (coordinate[1]+monitor[0],coordinate[0]+monitor[1])
                #     mouse.click(Button.left)
                
                # for value in coordinates:
                #     img[value[0],value[1]] = np.array((255,255,255,255))
                # cv.imshow("test",img)
                # cv.waitKey()
    listener.join()