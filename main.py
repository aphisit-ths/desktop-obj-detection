import cv2
import time
from PIL import Image
import numpy as np
import keyboard
from mss import mss

"""
1) pip install -r requirements.txta (ลงแค่ครั้งแรกที่ใช้งาน)
2) เปิดคอมเม้น cv2.imshow(...) เพื่อแสดงจุดที่โปรแกรมจะ detect 
3) ปรับค่าของ frame เพื่อปรับจุด 
4) ไปที่ cmd (ดู path ด้วย) พิม python main.py เพื่อรับ (หรือรันวิธีอื่นก็ได้) 
5) 
    if จุด detect ไม่ตรง:
        ให้ esc แล้วมาปรับ frame ไหม่ แล้วค่อย run อีกรอบ (มันไม่ปรับ realtime เพราะไม่ได้เขียนให้ทำงาน multi thread) 
    else if จุด detect ตรงแล้ว:
        สามารถปิดหรือเปิด cv2.imshow() ก็ได้
5) โปรแกรมนี้ทำงานเบื้องหน้าอย่างเดียวเหมาะสำหรับการเปิดทิ้งไว้โง่ๆ เท่านั้น
"""

# ปรับตรง frame ให้ตรงกับจุดที่ต้องการ detect
frame = {"top":780, "left":600, "width":700, "height":100}

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


#  A function for press something in game
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
            # ตรวจสอบว่า detect ครบสองครั้งหรือยัง ? 
            if status != 2:
                if area > 500:
                    print("Detected ==========================")
                    press_m()
                    increase_status()
                    # หลังาก detect จะหน่วงเวลาไว้ 1 วิ 
                    time.sleep(1)
            else:
                print("================== wait 5 sec for new game")
                reset_status()
                time.sleep(5)
                print("====================== start new game")
                press_m()

    print("======================================= กด esc เพื่อออกจากโปรแกรมm")

    # เปิดเพื่อ original เพื่อโชว์ว่ามันกำลัง detect ตรงไหนอยู่ ถ้าไม่ถูกต้องให้ไปปรับ frame ==============================================================>
    #cv2.imshow("original" ,img_raw)
    #cv2.imshow("mask image",mask0)

            
    if cv2.waitKey(25) & 0xFF == ord("Q"):
        cv2.destroyAllWindows()
        break;
