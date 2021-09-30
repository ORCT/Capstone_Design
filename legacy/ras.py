#라즈베리파이 USB 경로: /media/pi/ESD-USB/capstone/test_img/.....png
#리밋 스위치 초기 위치 잡는 코드 수정할 것

from numpy import cbrt
from printer.pylcd import detect_rising_edge
import printer
import serial
import os
import time
import cv2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

l_btn = 16
l_old_data = [0]
l_new_data = [0]
c_btn = 20
c_old_data = [0]
c_new_data = [0]
r_btn = 21
r_old_data = [0]
r_new_data = [0]

X_MAX = 291
 
path_dir = '/home/pi/Documents/capstone/test_img'

file_list = os.listdir(path_dir)
file_len = len(file_list)

if __name__ == "__main__":
    port = '/dev/ttyACM0'  # 변동가능
    ard = serial.Serial(port, 9600)
    ard.reset_input_buffer()
    ard.reset_output_buffer()
    
    state = -2
    state_m1_flag = 0
    state_0_cursor = 0
    state_0_flag = 1
    state_0_view = 0
    state_1_flag = 0
    state_1_interpolate_value = 0
    
    time.sleep(2.5)
    
    printer.interact_ser('!.bilinear.!.printer.`', ard)
    time.sleep(0.5)
    
    while True:
        if state == -2:
            if printer.detect_rising_edge(c_old_data, c_new_data, c_btn):
                state = 0
            
            try:
                file_list = os.listdir("/media/pi/ESD-USB/capstone/test_img")
                file_len = len(file_list)
                state = -1
                state_m1_flag = 1
            except:
                _ = 1
                
        if state == -1:
            if state_m1_flag == 1:
                printer.interact_ser('!USB on!ostart`', ard)
                state_m1_flag = 0
            if printer.detect_rising_edge(c_old_data, c_new_data, c_btn):
                state = 0
            
        
        if state == 0:
            if state_0_flag == 0:
                if printer.detect_rising_edge(r_old_data, r_new_data, r_btn):
                    if state_0_cursor < file_len - 1:
                        if state_0_view == 0:
                            state_0_view = 1
                        state_0_cursor += 1
                        state_0_flag = 1
                if printer.detect_rising_edge(l_old_data, l_new_data, l_btn):
                    if state_0_cursor > 0:
                        if state_0_view == 1:
                            state_0_view = 0
                        state_0_cursor -= 1
                        state_0_flag = 1
                if printer.detect_rising_edge(c_old_data, c_new_data, c_btn):
                    state = 1
                    state_1_flag = 1
                state_char_from_ard = ''
            
            if state_0_flag == 1:
                try:
                    if state_0_view == 0:
                        printer.interact_ser(f'!{file_list[state_0_cursor]}O!{file_list[state_0_cursor + 1]}`', ard)
                    else:
                        printer.interact_ser(f'!{file_list[state_0_cursor - 1]}!{file_list[state_0_cursor]}O`', ard)
                except:
                    _  = 1
                state_0_flag = 0
        
        if state == 1:
            if state_1_flag == 1:
                printer.interact_ser('!interpolation?!<y, >n `', ard)
                state_1_flag = 0
            if printer.detect_rising_edge(l_old_data, l_new_data, l_btn):
                state_1_interpolate_value = 1
                state = 2
                
            elif printer.detect_rising_edge(r_old_data, r_new_data, r_btn):
                state_1_interpolate_value = 0
                state = 2
                
        if state == 2:
            printer.interact_ser('!loading...`', ard)
            
            img = printer.load_image(path_dir + '/' + file_list[state_0_cursor], 'w')
            _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
            
            if state_1_interpolate_value == 0:
                _ = 1
            elif state_1_interpolate_value == 1:
                img = printer.distort_img(img)
            
            img = cv2.flip(img, 1)
            ser = printer.conv_img2ser(img)
            
            now_num = 0
            break_const = 0
            
            if img.shape[1] - 20 >= X_MAX:
                state = 4
                continue
            
            ser = ['d', '10', '`', 'i', '`', 'r', str((X_MAX - img.shape[1]) // 2), '`'] + ser
            
            all_num = printer.calc_all_ser(ser)
            
            for i in ser:
                printer.interact_ser(i, ard)
                
                if i.isdigit():
                    now_num += int(i)
                    print(f"percent: {round(now_num / all_num * 100, 2)}%")
                if i == '`':
                    printer.interact_ser(f'!{round(now_num / all_num * 100, 2)}%!opause`', ard)
                    if printer.detect_rising_edge(c_old_data, c_new_data, c_btn):
                        printer.interact_ser('!pause!<ctn, >stop`', ard)
                        init_step = int(printer.interact_ser('i`', ard))
                        while True:
                            if detect_rising_edge(l_old_data, l_new_data, l_btn):
                                printer.interact_ser('r' + str(init_step) + '`', ard)
                                break
                            elif detect_rising_edge(r_old_data, r_new_data, r_btn):
                                break_const = 1
                                break
                if break_const == 1:
                    break
                    
            state = 0
            state_0_flag = 1

        if state == 4:
            printer.interact_ser(f"!img too long.!img < {X_MAX - 30}`", ard)
            time.sleep(2)
            state = 0
            state_0_flag = 1