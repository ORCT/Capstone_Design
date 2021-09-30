import cv2
import numpy as np
from collections import deque
import printer
import serial
import time
import pyautogui

img = printer.load_image("test/test2_output.png", 'w')
img = cv2.flip(img, 1)
_, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

print(img.shape)
ser = printer.conv_img2ser(img)

print(ser)

conv_img = printer.conv_ser2img(ser, img.shape)

ser = ['d', '10', '`', 'i', '`', 'r', '5', '`'] + ser
all_num = printer.calc_all_ser(ser)

print(all_num, img.shape[0] * img.shape[1])
print(f"사용률: (출력 전체 step: {all_num}) / (이미지 전체 step: {img.shape[0] * img.shape[1]}) = {all_num / img.shape[0] / img.shape[1]}")

if __name__ == "__main__":
    port = 'COM12'  # 변동가능
    ard = serial.Serial(port, 9600)
    time.sleep(2)
    
    now_num = 0
    start_time = time.time()

    for i in ser:
        while list(pyautogui.position()) == [0, 0]:
            _ = 1
            
        printer.interact_ser(i, ard)
        
        if i.isdigit():
            now_num += int(i)
            print(f"percent: {round(now_num / all_num * 100, 2)}%, estimated: {round((all_num - now_num) * 0.012 , 2)}s")

    print((all_num) / (time.time() - start_time))
    print((time.time() - start_time) / (all_num))
    ard.close()
