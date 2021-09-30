import tkinter
from collections import deque
import tkinter.ttk
import os
import cv2
import printer
import serial
from printer.serial_test import interact_ser
import threading

root = tkinter.Tk()
root.title("Printer")
root.geometry("300x300")


try:
    path_dir = '/home/pi/Documents/capstone/test_img'
    file_list = os.listdir(path_dir)
except:
    path_dir = 'test'
    file_list = os.listdir(path_dir)
file_len = len(file_list)


global_port = "COM11"
global_ard = serial.Serial(global_port, 9600)
global_X_MAX = 291
global_state = 0 # basic state
global_deque = deque() # serial deque
global_current_process = 0
global_all_process = 0
global_thread = 0

def print_deque():
    global global_port
    global global_ard
    global global_X_MAX
    global global_state
    global global_deque
    global global_current_process
    global global_all_process
    while len(global_deque) != 0:
        if global_deque[0] == 'p' and global_state == 2:
            while global_state != 1:
                _ = 1
                if global_state == 0:
                    break
        if len(global_deque) == 0:
            break
        if global_deque[0] == 'p' and global_state == 0:
            break
        tmp = global_deque.popleft()
        output = printer.interact_ser(tmp, global_ard)
        
        if output != None:
            serial_monitor_txt.delete("1.0","end")
            serial_monitor_txt.insert(tkinter.END, output[:-2])
        
        if tmp.isdigit():
            global_current_process += int(tmp)
            
            percent_txt.delete("1.0","end")
            percent_txt.insert(tkinter.END, f"{round(global_current_process / global_all_process * 100, 2)}%")

    stop_print()
    print("thread end")




combobox1_str = tkinter.StringVar()
combobox1_values = file_list
checkbutton1_int = tkinter.IntVar()


def play_pause_print():
    global global_port
    global global_ard
    global global_X_MAX
    global global_state
    global global_deque
    global global_current_process
    global global_all_process
    global global_thread
    if global_state == 0:
        
        global_thread = threading.Thread(target=print_deque)
        
        print_state_txt.delete("1.0","end")
        print_state_txt.insert(tkinter.END, "image loading...")
        
        img = cv2.imread(path_dir + '/' + combobox1_str.get(), cv2.IMREAD_GRAYSCALE)
        _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        
        if checkbutton1_int.get() == 0:
            _ = 1
        else:
            img = printer.distort_img(img)
            
        img = cv2.flip(img, 1)
        
        if img.shape[1] - 20 >= global_X_MAX:
            print_state_txt.delete("1.0","end")
            print_state_txt.insert(tkinter.END, "image is too big!")
            
        else:
            global_deque = deque(['d', '10', '`', 'i', '`', 'r', str((global_X_MAX - img.shape[1]) // 2), '`'] + printer.conv_img2ser(img))
            global_all_process = printer.calc_all_ser(global_deque)
            
            
            print_state_txt.delete("1.0","end")
            print_state_txt.insert(tkinter.END, "image load end")

        global_state = 1
        global_thread.daemon = True
        global_thread.start()
            
        
        
    elif global_state == 1:
        print_state_txt.delete("1.0","end")
        print_state_txt.insert(tkinter.END, "pasue")
        global_state = 2
        
    elif global_state == 2:
        print_state_txt.delete("1.0","end")
        print_state_txt.insert(tkinter.END, "resume")
        global_state = 1
        
def stop_print():
    global global_port
    global global_ard
    global global_X_MAX
    global global_state
    global global_deque
    global global_current_process
    global global_all_process
    global global_thread
    if global_state == 1 or global_state == 2:
        global_thread = 0
        global_state = 0
        global_deque = deque()
        global_current_process = 0
        global_all_process = 0
        serial_monitor_txt.delete("1.0","end")
        percent_txt.delete("1.0","end")
        print_state_txt.delete("1.0","end")
        print_state_txt.insert(tkinter.END, "init")


# button init

printer_frame = tkinter.ttk.Labelframe(root, text='printer option')
printer_frame.place(x=5, y=5, width=200, height=280)

play_pause_btn = tkinter.Button(root, text="print play/pause", command=play_pause_print)
play_pause_btn.place(x=10, y=70, width=190, height=40)

stop_btn = tkinter.Button(root, text="print stop", command=stop_print)
stop_btn.place(x=10, y=110, width=190, height=40)


# checkbox & label init

file_option_label = tkinter.Label(root, anchor='w', text='file option:')
file_option_label.place(x=10, y= 25, width=60, height=20)


file_combobox = tkinter.ttk.Combobox(root, textvariable=combobox1_str, values=combobox1_values)
file_combobox.place(x=75, y= 25, width=125, height=20)
file_combobox.current(0)

distortion_checkbutton = tkinter.Checkbutton(root, text="distortion option", variable=checkbutton1_int)
distortion_checkbutton.place(x=10, y= 45)

serial_monitor_label = tkinter.Label(root, anchor='w', text='serial monitor')
serial_monitor_label.place(x=10, y= 160, width=190, height=20)

serial_monitor_txt = tkinter.Text(root)
serial_monitor_txt.pack()
serial_monitor_txt.place(x=10, y=180, width=190, height=20)

percent_label = tkinter.Label(root, anchor='w', text='percent')
percent_label.place(x=10, y= 200, width=190, height=20)

percent_txt = tkinter.Text(root)
percent_txt.pack()
percent_txt.place(x=10, y=220, width=190, height=20)

print_state_label = tkinter.Label(root, anchor='w', text='print state')
print_state_label.place(x=10, y= 240, width=190, height=20)

print_state_txt = tkinter.Text(root)
print_state_txt.pack()
print_state_txt.place(x=10, y=260, width=190, height=20)

root.mainloop()