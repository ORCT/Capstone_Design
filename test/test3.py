# serial protocol: 
# 1. All serial protocol consists of two independent strings.
# 2. First string is one of the following:
# - p -> push solenoid
# - P -> pull solenoid
# - r -> right mov
# - l -> left mov
# - d -> down mov
# - ` -> end sub serial bundle
# * But 'p' and 'P' hasn't number string. 
#
# 3. Second string is a integer number.
#
# * So, protocol has the following forms.
# ['p', `, 'r', '23', `, 'P', `, 'r', '2', `, 'd', '1', `, 'P', `, 'l', '23', `, ...]
#
#

import cv2
import numpy as np
from collections import deque

def conv_img_to_ser_deque(img):
    threshold_val = 255
    m, n = img.shape
    ans_deque = deque()
    cnt = 0
    lr_flag = -1
    sol_flag = 0
    for row in img:
        row_deque = deque(row)
        if threshold_val not in row_deque:
            if lr_flag == -1:
                lr_flag = 0
                cnt = 1
            else:
                cnt += 1
        else:
            if lr_flag == -1:
                lr_flag = 0
            else:
                if sol_flag == 1:
                    ans_deque.append('P')
                    ans_deque.append('`')
                ans_deque.append('d')
                ans_deque.append(str(cnt))
                ans_deque.append('`')
            
            cnt = 1
            edge = -1
            tmp = 0
            if lr_flag == 0:
                while row_deque:
                    tmp = row_deque.popleft()
                    if tmp == 0 and edge == -1:
                        ans_deque.append('r')
                        edge = 0
                    elif tmp == threshold_val and edge == -1:
                        ans_deque.append('p')
                        ans_deque.append('`')
                        ans_deque.append('r')
                        edge = 1
                    elif tmp == 0 and edge == 0:
                        cnt += 1
                    elif tmp == threshold_val and edge == 1:
                        cnt += 1
                    elif tmp == 0 and edge == 1:
                        ans_deque.append(str(cnt))
                        ans_deque.append('`')
                        ans_deque.append('P')
                        ans_deque.append('`')
                        ans_deque.append('r')
                        edge = 0
                        cnt = 1
                    elif tmp == threshold_val and edge == 0:
                        ans_deque.append(str(cnt))
                        ans_deque.append('`')
                        ans_deque.append('p')
                        ans_deque.append('`')
                        ans_deque.append('r')
                        edge = 1
                        cnt = 1
                if edge == 1 and tmp == threshold_val or edge == 0 and tmp == 0:
                    ans_deque.append(str(cnt))
                    ans_deque.append('`')
                sol_flag = 0 if edge == 0 else 1
                cnt = 1
                lr_flag = (lr_flag + 1) % 2

            if lr_flag == 1:
                while row_deque:
                    tmp = row_deque.pop()
                    if tmp == 0 and edge == -1:
                        ans_deque.append('l')
                        edge = 0
                    elif tmp == threshold_val and edge == -1:
                        ans_deque.append('p')
                        ans_deque.append('`')
                        ans_deque.append('l')
                        edge = 1
                    elif tmp == 0 and edge == 0:
                        cnt += 1
                    elif tmp == threshold_val and edge == 1:
                        cnt += 1
                    elif tmp == 0 and edge == 1:
                        ans_deque.append(str(cnt))
                        ans_deque.append('`')
                        ans_deque.append('P')
                        ans_deque.append('`')
                        ans_deque.append('l')
                        edge = 0
                        cnt = 1
                    elif tmp == threshold_val and edge == 0:
                        ans_deque.append(str(cnt))
                        ans_deque.append('`')
                        ans_deque.append('p')
                        ans_deque.append('`')
                        ans_deque.append('l')
                        edge = 1
                        cnt = 1
                if edge == 1 and tmp == threshold_val or edge == 0 and tmp == 0:
                    ans_deque.append(str(cnt))
                    ans_deque.append('`')
                sol_flag = 0 if edge == 0 else 1
                cnt = 1
                lr_flag = (lr_flag + 1) % 2
    ans_deque.append(str(cnt))
    ans_deque.append('`')
    return ans_deque
            

def conv_ser_deque_to_img(ser_deque, img_shape):
    threshold_val = 255
    ans_img = np.zeros(img_shape)
    x, y = 0, 0
    solenoid_state = 0
    while ser_deque:
        tmp = ser_deque.popleft()
        if tmp == 'd':
            y += int(ser_deque.popleft())
        elif tmp == 'p':
            solenoid_state = 1
            ser_deque.popleft()
        elif tmp == 'P':
            solenoid_state = 0
            ser_deque.popleft()
        elif tmp == 'r':
            r_mov_dis = int(ser_deque.popleft())
            _ = ser_deque.popleft()
            while r_mov_dis != 0:
                if solenoid_state == 1:
                    ans_img[y][x] = threshold_val
                x += 1
                r_mov_dis -= 1
        elif tmp == 'l':
            l_mov_dis = int(ser_deque.popleft())
            _ = ser_deque.popleft()
            while l_mov_dis != 0:
                x -= 1
                if solenoid_state == 1:
                    ans_img[y][x] = threshold_val
                l_mov_dis -= 1
    return ans_img

if __name__ == "__main__":
    img = cv2.imread('test/test1.png', cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (0, 0), fx=0.05, fy=0.05)
    _, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    cv2.imwrite('test/test2.png', img)
    serial_deque = conv_img_to_ser_deque(img)

    print(img)

    for i in serial_deque:
        print(i, end=' ')

    conv_img = conv_ser_deque_to_img(serial_deque, img.shape)
    cv2.imwrite('test/test3.png', conv_img)

    # n, m = img.shape
    # for i in range(n):
    #     for j in range(m):
    #         if img[i][j] != conv_img[i][j]:
    #             print('False', i, j)
