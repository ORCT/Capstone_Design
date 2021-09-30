import tkinter
import tkinter.ttk  





root = tkinter.Tk()
root.title("Braille Printer")
root.geometry("1400x750")

gui_global_state = 0

def func1():
    global gui_global_state
    print(combobox1_str.get())
    gui_global_state = 1

def func2():
    global gui_global_state
    gui_global_state = 2

def func3():
    global gui_global_state
    gui_global_state = 3

def func4():
    global gui_global_state
    gui_global_state = 4

btn1 = tkinter.Button(root, text="btn1", command=func1)
btn1.place(x=0, y=0, width=100, height=40)

btn2 = tkinter.Button(root, text="btn2", command=func2)
btn2.place(x=0, y=40, width=100, height=40)

btn3 = tkinter.Button(root, text="btn3", command=func3)
btn3.place(x=0, y=80, width=100, height=40)

btn4 = tkinter.Button(root, text="btn4", command=func4)
btn4.place(x=0, y=120, width=100, height=40)

combobox1_str = tkinter.StringVar()
combobox1 = tkinter.ttk.Combobox(root, textvariable=combobox1_str, values=[1, 2, 3, 4])
combobox1.place(x=0, y= 160, width=100, height=20)
combobox1.current(0)



''' 
main_txt = tkinter.Text(root)
main_txt.pack()
main_txt.place(x=100, y=0, width=400, height=750)

cursor_txt = tkinter.Text(root)
cursor_txt.pack()
cursor_txt.place(x=0, y=180, width=100, height=20)

state_txt = tkinter.Text(root)
state_txt.pack()
state_txt.place(x=0, y=200, width=100, height=550) '''

root.mainloop()