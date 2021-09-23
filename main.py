import printer
import cv2
import numpy as np
import serial
import time
import pyautogui
from collections import deque

n = '8'

image = cv2.imread("input" + n + ".png", cv2.IMREAD_GRAYSCALE)
image = 255 - image
img_y, img_x = image.shape
print(img_x, img_y)

a = 2000
h = 130
y = 39

image = cv2.resize(image, dsize=(0, 0), fx=y / img_y, fy=y / img_y, interpolation=cv2.INTER_LINEAR)
img_y, img_x = image.shape
x = img_x
Y = int(a * y / (h - y))
X = int(x * (Y + a) / a)
print(X, Y)
print(img_x, img_y)

if X >= 195: # 제한 크기
    raise Exception("X-axis limit")

p1 = (0, 0)
p2 = (0,    X)
p3 = (Y, X // 2 - img_x // 2)
p4 = (Y, X // 2 + img_x // 2)
name = printer.bilinear_interpolate(image, p1, p2, p3, p4)
_, name = cv2.threshold(name, 100, 255, cv2.THRESH_BINARY)
name = cv2.GaussianBlur(name, (3,3), 0)
_, img = cv2.threshold(name, 1, 255, cv2.THRESH_BINARY)

img = cv2.resize(img, (0, 0), fx=1, fy=1)
_, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
cv2.imwrite("output" + n + ".png", img)
serial_deque = printer.conv_img_to_ser_deque(img)

serial_deque.appendleft('`')
serial_deque.appendleft('5')
serial_deque.appendleft('r')
serial_deque.appendleft('`')
serial_deque.appendleft('i')

def interact_ser(_str, _ard):
    _ard.write(_str.encode())
    tmp = _ard.readline()
    print(tmp.decode())
    

if __name__ == "__main__":
    port = 'COM11'  # 변동가능
    ard = serial.Serial(port, 9600)
    time.sleep(2)

    for i in serial_deque:
        if list(pyautogui.position()) != [0, 0]:
            interact_ser(i, ard)

    ard.close()
