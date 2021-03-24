from img_serial_v02 import *
from serial_test_v01 import *
import time

port = 'COM6' #변동가능
ard = serial.Serial(port, 9600)

img = cv2.imread('no1.jpg', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
_, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
cv2.imwrite('test1.png', img)
serial_deque = conv_img_to_ser_deque(img)

while serial_deque:
    tmp_str = serial_deque.popleft()
    for send_str in tmp_str:
        interact_ser(send_str, ard)
        time.sleep(0.001)

ard.close()