import cv2
import time
from PIL import Image
from hamcrest import none
import numpy as np
import keyboard
from mss import mss
import tkinter as tk
screen_manager = mss()
lower_red = np.array([0,50,50])
upper_red = np.array([10,255,255])
is_exit = False
status = 0
def reset_status():
    global status
    status = 0
def increase_status():
    global status
    status +=1
def exit():
    global is_exit
    is_exit = True
    print("=====> Exit Program")

keyboard.add_hotkey("esc", exit) 
#ปรับตรง frame
frame = {"top":780, "left":600, "width":700, "height":100}

#  A function for press somthing in game
def press_m():
    keyboard.press("m")

while True:
    if is_exit:
        break;
    screenshot = screen_manager.grab(frame)
    image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
    #raw image
    img_raw = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    #hsv image for detection
    cvt = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2HSV)
            
    mask0 = cv2.inRange(cvt, lower_red, upper_red)
            
    contours , hierarchy = cv2.findContours(mask0 ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
            
    if len(contours) != 0:
        for contour in contours:
            area = cv2.contourArea(contour)
            if status != 2:
                if area > 500:
                    print("Detected ==================>")
                    press_m()
                    increase_status()
                    time.sleep(1)
            else:
                print("==================พักก่อนน")
                reset_status()
                time.sleep(3)

    print("=======================================>")
    #cv2.imshow("mask image",mask0)
    #cv2.imshow("original" ,img_raw)
            
    if cv2.waitKey(25) & 0xFF == ord("Q"):
        cv2.destroyAllWindows()
        break;
