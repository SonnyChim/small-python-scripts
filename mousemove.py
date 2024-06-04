from pynput import keyboard
from pynput.mouse import Button,Controller
import time

def on_press(key):
    global up,left,down,right
    if key == keyboard.Key.esc:
        global liston
        liston = False
        return False
    try:
        k = key.char
    except:
        k = key.name
    if k in ["i","j","k","l","u","h","o","p"]:
        if k == "i":
            up = True
            print("up")
        if k == "j":
            left = True
            print("left")
        if k == "k":
            down = True
            print("down")
        if k == "l":
            right = True
            print("right")
        if k == "u":
            mouse.scroll(0,1)
        if k == "h":
            mouse.scroll(0,-1)
        if k == "o":
            mouse.press(Button.left)
        if k == "p":
            mouse.press(Button.right)

def on_release(key):
    global up,left,down,right
    if key == keyboard.Key.esc:
        return False
    try:
        k = key.char
    except:
        k = key.name
    if k in ["i","j","k","l","o","p"]:
        if k == "i":
            up = False
        if k == "j":
            left = False
        if k == "k":
            down = False
        if k == "l":
            right = False
        if k == "o":
            mouse.release(Button.left)
        if k == "p":
            mouse.release(Button.right)

mouse = Controller()
liston = True
dm = 20
up = False
left = False
down = False
right = False
tup = 0
tleft = 0
tdown= 0
tright = 0
listener = keyboard.Listener(on_press=on_press,on_release=on_release)
listener.start()
while liston:
    tnow = time.perf_counter_ns()
    if up and tup <= tnow :
        tup = tnow + 1000000
        mouse.move(0,-1)
    if left and tleft <= tnow :
        tleft = tnow + 1000000
        mouse.move(-1,0)
    if down and tdown <= tnow :
        tdown = tnow + 1000000
        mouse.move(0,1)
    if right and tright <= tnow :
        tright = tnow + 1000000
        mouse.move(1,0)
listener.join()