import serial

def interact_ser(_str, _ard):
    _ard.write(_str.encode())
    tmp = _ard.readline()
    print(tmp.decode())

if __name__ == "__main__":
    port = 'COM7' #변동가능
    ard = serial.Serial(port, 9600)

    while True:
        send_str = input()
        if send_str == '1':
            break
        else:
            interact_ser(send_str, ard)
    
    ard.close()