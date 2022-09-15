
import serial
import time
from tkinter import messagebox

def serialConnect(*args):
    #mapping of the cli commands and parsing the commands thru serial port"
    clkButton = args[0].cget(('text'))
    portid =args[1]
    baud = args[2]
    lines =[]
    wait_time = 0.1
    print (clkButton)
    cmdDict = { "BUZZER TEST":'buz 2', "BLUE LED TEST":'led 1', "DISPLAY LED TEST":'lcd 1',"Valve-Open": 'valve 1',
                "Valve-Close":'valve 0',"Regulator Lock": 'servo 40','UnLock': 'servo 80',
                "Self Test": 'self',"Active Mode": 'mode 1',"Gas-On":'sens 1',"Gas-Off":'sens 1',
                "Remove": 'sens 1',"MCU Stop Current": 'stop',"GSM Stop Current":'stop', 
                'Mode 0':'mode 0', 'Mode 1': 'mode 1', 'Mode 2':'mode 2'
                }
    if clkButton in cmdDict.keys():
        cmd = cmdDict.get(clkButton)
    if cmd == 'self':
        wait_time = 1
    try:
        ser = serial.Serial(
        port=portid,
        baudrate=baud,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)
        if ser.isOpen():
            #print(ser.name)
            ser.close()
        ser.open()
        #print(ser.isOpen())
        serialData =True
        cmd = cmd +'\r\n'
        if ser.in_waiting == 0:
            ser.write(cmd.encode('utf-8'))
            time.sleep(0.2)
            print("command done")

    except:
        messagebox.showerror("ERROR",'Please Check your portID or BaudRate')
    
