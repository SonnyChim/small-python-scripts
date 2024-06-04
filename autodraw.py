from mss.windows import MSS as mss
import numpy as np
import cv2 as cv
from pynput import keyboard
from pynput.mouse import Controller,Button
import time

def on_press(key):
    global running,listening,reset
    if key == keyboard.Key.esc:
        listening = False
        return False
    if key == keyboard.Key.f8:
        running = not running
        # draw_img(mouse.position[0],mouse.position[1])
    if key == keyboard.Key.f9:
        reset = True

def draw_img(x,y):  
    img = cv.imread("ditheringOut.png")
    values = np.nonzero(img == (0,0,0))
    values = np.rot90(values,3)
    for value in values:
        # time.sleep(0.001)
        mouse.position = (value[1]+x,value[2]+y)
        mouse.press(Button.left)
        mouse.release(Button.left)


with keyboard.Listener(on_press=on_press) as listener:
    with  Controller() as mouse: 
        listening = True
        running = False
        i = 0
        reset = True
        scale = 1
        skip = 1
        while listening:
            if reset:
                img = cv.imread("ditheringOut.png")
                values = np.nonzero(img == (0,0,0))
                values = np.rot90(values,3)
                i = 0
                stop = values.shape[0]
                x,y = mouse.position
                reset = False
            if running:
                while running and i < stop:
                    value = values[i]
                    mouse.position = ((value[1])*scale+x,(value[2])*scale+y)
                    mouse.press(Button.left)
                    mouse.release(Button.left)
                    time.sleep(0.001)
                    i += skip
                running = False
        listener.join()