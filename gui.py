import tkinter
from collections import deque
import tkinter.ttk
import os
import cv2
import printer
import serial

from printer.serial_test import interact_ser

X_MAX = 291

try:
    path_dir = '/home/pi/Documents/capstone/test_img'
    file_list = os.listdir(path_dir)
    
except:
    path_dir = 'test'
    file_list = os.listdir(path_dir)
file_len = len(file_list)



root = tkinter.Tk()
root.title("Printer")
root.geometry("300x300")

gui_global_state = 0 # basic state
gui_global_state1_flag = 0 # 0 is pause, 1 is play
gui_global_deque = deque() # serial deque
gui_global_print_flag = 0 # 0 remains nothing, 1 remains residue
gui_global_port = "COM11"
gui_global_ard = serial.Serial(gui_global_port, 9600)

combobox1_str = tkinter.StringVar()
combobox1_values = file_list
checkbutton1_int = tkinter.IntVar()

def func1():
    global gui_global_state
    global gui_global_state1_flag
    global gui_global_deque
    global gui_global_print_flag
    global gui_global_ard
    
    txt3.delete("1.0","end")
    
    if gui_global_state1_flag == 0:
        if gui_global_print_flag == 0:
            txt3.delete("1.0","end")
            txt3.insert(tkinter.END, "image loading...")
            img = cv2.imread(path_dir + '/' + combobox1_str.get(), cv2.IMREAD_GRAYSCALE)
            _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
            
            if checkbutton1_int.get() == 0:
                _ = 1
            else:
                img = printer.distort_img(img)
                
            img = cv2.flip(img, 1)
            
            if img.shape[1] - 20 >= X_MAX:
                txt3.delete("1.0","end")
                txt3.insert(tkinter.END, "image is too big!")
            else:
                gui_global_deque = deque(['d', '10', '`', 'i', '`', 'r', str((X_MAX - img.shape[1]) // 2), '`'] + printer.conv_img2ser(img))
                txt1.delete("1.0","end")
                txt1.insert(tkinter.END, "image load end")
                gui_global_state1_flag = 1
                gui_global_print_flag = 1
            
        else:
            gui_global_state1_flag = 1
        
    if gui_global_state1_flag == 1:
        deque_len = len(gui_global_deque)
        for i in range(deque_len):
            tmp = gui_global_deque.popleft()
            interact_ser(tmp, gui_global_ard)
            txt3.delete("1.0","end")
            txt3.insert(tkinter.END, tmp)
            
        if len(gui_global_deque) == 0:
            txt3.delete("1.0","end")
            txt3.insert(tkinter.END, "printing end")
            gui_global_state1_flag = 0
    
    gui_global_state = 1

def func2():
    global gui_global_state
    print(checkbutton1_int.get())
    gui_global_state = 2


# button init

frame1 = tkinter.ttk.Labelframe(root, text='printer option')
frame1.place(x=5, y=5, width=200, height=280)

btn1 = tkinter.Button(root, text="print play/pause", command=func1)
btn1.place(x=10, y=70, width=190, height=40)

btn2 = tkinter.Button(root, text="print stop", command=func2)
btn2.place(x=10, y=110, width=190, height=40)


# checkbox & label init

label0 = tkinter.Label(root, anchor='w', text='file option:')
label0.place(x=10, y= 25, width=60, height=20)


combobox1 = tkinter.ttk.Combobox(root, textvariable=combobox1_str, values=combobox1_values)
combobox1.place(x=75, y= 25, width=125, height=20)
combobox1.current(0)

checkbutton1 = tkinter.Checkbutton(root, text="distortion option", variable=checkbutton1_int)
checkbutton1.place(x=10, y= 45)

label1 = tkinter.Label(root, anchor='w', text='serial monitor')
label1.place(x=10, y= 160, width=190, height=20)

txt1 = tkinter.Text(root)
txt1.pack()
txt1.place(x=10, y=180, width=190, height=20)

label2 = tkinter.Label(root, anchor='w', text='percent')
label2.place(x=10, y= 200, width=190, height=20)

txt2 = tkinter.Text(root)
txt2.pack()
txt2.place(x=10, y=220, width=190, height=20)

label3 = tkinter.Label(root, anchor='w', text='print state')
label3.place(x=10, y= 240, width=190, height=20)

txt3 = tkinter.Text(root)
txt3.pack()
txt3.place(x=10, y=260, width=190, height=20)

root.mainloop()