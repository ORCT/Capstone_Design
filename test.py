import cv2
import numpy as np
from collections import deque

# _state: 글자 색 상태

def load_image(_img, _state='w'):
    _img = cv2.imread(_img, cv2.IMREAD_GRAYSCALE)
    if _state == 'b':
        _img = 255 - _img
    ans = _img
    return ans

def conv_img2ser(_img):
    Y, X = _img.shape
    y, x = 0, 0
    ans1 = []
    
    init_loc = [0, 0]
    
    for i in range(Y - 1):
        for j in range(X - 1):
            if _img[y, x] == 255:
                ans1.append('p')
                ans1.append('`')
                ans1.append('P')
                ans1.append('`')
            if y % 2 == 0:
                ans1.append('r')
                ans1.append('1')
                ans1.append('`')
                x += 1
            if y % 2 == 1:
                ans1.append('l')
                ans1.append('1')
                ans1.append('`')
                x -= 1
                
        ans1.append('d')
        ans1.append('1')
        ans1.append('`')
        y += 1
        
    return ans1

def conv_ser2img(_ser, _img_shape):
    ans = np.zeros(_img_shape)
    x, y = 0, 0
    
    i = 0
    while i < len(_ser):
        if _ser[i] == 'p':
            ans[y, x] = 255
        elif _ser[i] == 'r':
            i += 1
            x += int(_ser[i])
        elif _ser[i] == 'l':
            i += 1
            x -= int(_ser[i])
        elif _ser[i] == 'd':
            i += 1
            y += int(_ser[i])
        i += 1
    
    return ans
        
n = '9'        

a = load_image("input" + n + ".png", 'w')

print(a.shape)

ser = conv_img2ser(a)


print(ser)

img = conv_ser2img(ser, a.shape)


cv2.imwrite("test.png", a)
cv2.imwrite("test_conv.png", a)