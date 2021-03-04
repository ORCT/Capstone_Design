import serial

def ser(al, ard):
    ard.write(al.encode())
    y = ard.readline()
    print(y.decode())

port = 'COM7'
ard = serial.Serial(port, 9600)

x = ard.readline()
print(x.decode())

while True:
    k = input()
    if k == "1":
        break
    else:
        ser(k, ard)

ard.close()