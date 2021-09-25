import cv2
import numpy as np
from collections import deque
import printer
import serial
import time
import pyautogui

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
    _state = 0
    ans1 = []
    
    while _state != 3:
        if _state == 0:
            if 255 in _img[y]:
                _state = 2
            else:
                _state = 1
                
        elif _state == 1:
            _down_flag = 0
            for i in range(y + 1, Y):
                if 255 in _img[i]:
                    _down_flag = 1
                    ans1.append('d')
                    ans1.append(str(i - y))
                    ans1.append('`')
                    y = i
                    break
            if _down_flag == 0:
                _state = 3
            elif _down_flag == 1:
                _state = 2
                
        elif _state == 2:
            _r_max = 0
            _l_max = 0
            for i in range(X):
                if _img[y, i] == 255:
                    _l_max = i
                    break
            for i in range(X):
                if _img[y, X - 1 - i] == 255:
                    _r_max = X - 1 - i
                    break
            
            _r_dis = abs(x - _r_max)
            _l_dis = abs(x - _l_max)
            
            if _r_dis >= _l_dis:
                if x - _l_max > 0:
                    ans1.append('l')
                    ans1.append(str(x - _l_max))
                    ans1.append('`')
                elif x - _l_max < 0:
                    ans1.append('r')
                    ans1.append(str(_l_max - x))
                    ans1.append('`')
                x = _l_max
                    
                
                _push_flag = 0
                
                while x <= _r_max:
                    if _img[y, x] == 255:
                        if _push_flag == 0:
                            ans1.append('p')
                            ans1.append('`')
                            ans1.append('P')
                            ans1.append('`')
                            ans1.append('r')
                            ans1.append('1')
                            ans1.append('`')
                            _push_flag = 1
                        elif _push_flag == 1:
                            ans1.pop()
                            ans1.pop()
                            ans1.pop()
                            ans1.pop()
                            ans1.pop()
                            ans1.append('r')
                            ans1.append('1')
                            ans1.append('`')
                            ans1.append('P')
                            ans1.append('`')
                            ans1.append('r')
                            ans1.append('1')
                            ans1.append('`')
                    else:
                        _push_flag = 0
                        ans1.append('r')
                        ans1.append('1')
                        ans1.append('`')
                    if x < _r_max:
                        x += 1
                    else:
                        ans1.pop()
                        ans1.pop()
                        ans1.pop()
                        break
                
            elif _r_dis < _l_dis:
                if _r_max - x > 0:
                    ans1.append('r')
                    ans1.append(str(_r_max - x))
                    ans1.append('`')
                elif _r_max - x < 0:
                    ans1.append('l')
                    ans1.append(str(x - _r_max))
                    ans1.append('`')
                x = _r_max
                
                _push_flag = 0
                
                while x >= _l_max:
                    if _img[y, x] == 255:
                        if _push_flag == 0:
                            ans1.append('p')
                            ans1.append('`')
                            ans1.append('P')
                            ans1.append('`')
                            ans1.append('l')
                            ans1.append('1')
                            ans1.append('`')
                            _push_flag = 1
                        elif _push_flag == 1:
                            ans1.pop()
                            ans1.pop()
                            ans1.pop()
                            ans1.pop()
                            ans1.pop()
                            ans1.append('l')
                            ans1.append('1')
                            ans1.append('`')
                            ans1.append('P')
                            ans1.append('`')
                            ans1.append('l')
                            ans1.append('1')
                            ans1.append('`')
                    else:
                        _push_flag = 0
                        ans1.append('l')
                        ans1.append('1')
                        ans1.append('`')
                    if x > _l_max:
                        x -= 1
                    else:
                        ans1.pop()
                        ans1.pop()
                        ans1.pop()
                        break
                    
            _state = 1
        
    ans1 = deque(ans1)
    ans2 = []
    while ans1:
        tmp = ans1.popleft()
        try:
            if tmp == 'r' and ans1[2] == 'r':
                down_num = int(ans1[0])
                ans1.popleft()
                ans1.popleft()
                ans1[1] = str(down_num + 1)
                
            elif tmp == 'l' and ans1[2] == 'l':
                down_num = int(ans1[0])
                ans1.popleft()
                ans1.popleft()
                ans1[1] = str(down_num + 1)
                
            elif tmp == 'd' and ans1[2] == 'd':
                down_num = int(ans1[0])
                ans1.popleft()
                ans1.popleft()
                ans1[1] = str(down_num + 1)
            else:
                ans2.append(tmp)
                
        except:
            ans2.append(tmp)
        
    return ans2

def conv_ser2img(_ser, _img_shape):
    ans = np.zeros(_img_shape)
    x, y = 0, 0
    i = 0
    
    push_flag = 0
    dir_flag = ''
    while i < len(_ser):
        tmp = _ser[i]
        if tmp == 'p':
            ans[y, x] = 255
            push_flag = 1
        elif tmp == 'P':
            push_flag = 0
        elif tmp == 'd':
            dir_flag = 'd'
        elif tmp == 'r':
            dir_flag = 'r'
        elif tmp == 'l':
            dir_flag = 'l'
        elif tmp.isdigit():
            tmp = int(tmp)
            if dir_flag == 'd':
                if push_flag == 0:
                    y += tmp
                elif push_flag == 1:
                    for _ in range(tmp):
                        y += 1
                        ans[y, x] = 255
            
            elif dir_flag == 'r':
                if push_flag == 0:
                    x += tmp
                elif push_flag == 1:
                    for _ in range(tmp):
                        x += 1
                        ans[y, x] = 255
                
            elif dir_flag == 'l':
                if push_flag == 0:
                    x -= tmp
                elif push_flag == 1:
                    for _ in range(tmp):
                        x -= 1
                        ans[y, x] = 255
            
            dir_flag = ''
        elif tmp == '`':
            _ = 1
        i += 1
    return ans

def calc_all_ser(_ser):
    ans = 0
    for i in _ser:
        if i.isdigit():
            ans += int(i)
    return ans

### main        

a = load_image("input8.png", 'b')
a = cv2.flip(a, 1)

print(a.shape)
ser = conv_img2ser(a)
all_num = calc_all_ser(ser)

print(all_num, a.shape[0] * a.shape[1])
print(f"사용률: (출력 전체 step: {all_num}) / (이미지 전체 step: {a.shape[0] * a.shape[1]}) = {all_num / a.shape[0] / a.shape[1]}")

print(ser)
img = conv_ser2img(ser, a.shape)

#ser = ['d', '10', '`', 'i', '`', 'r', '5', '`'] + ser



cv2.imwrite("test.png", a)
cv2.imwrite("test_conv.png", a)

if __name__ == "__main__":
    port = 'COM7'  # 변동가능
    ard = serial.Serial(port, 9600)
    time.sleep(2)
    
    now_num = 0
    start_time = time.time()

    
    for i in ser:
        if list(pyautogui.position()) != [0, 0]:
            printer.interact_ser(i, ard)
        
        if i.isdigit():
            now_num += int(i)
            print(f"percent: {round(now_num / all_num * 100, 2)}%, estimated: {round((all_num - now_num) * 0.012 , 2)}s")

    print((all_num) / (time.time() - start_time))
    print((time.time() - start_time) / (all_num))
    ard.close()
