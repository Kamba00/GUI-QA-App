import serial
import serial.tools.list_ports
from tkinter import messagebox

def serialConnect(args):
    global ser_init
    #mapping of the cli commands and parsing the commands thru serial port"
    clkButton = args
    #print (clkButton)
    cmdDict = {'Buzzer':'buz 2', 
                'LED':'led 1', 
                'Display':'lcd 1',
                "Shutoff Valve": 'valve 1',
                "Regulator Lock": 'servo 50',
                'UnLock': 'servo 65',
                "GSM": 'gsm 1',
                "Self Test": 'self 1',
                "Active Mode": 'mode 1',
                "Gas-On":'sens 1',
                "Gas-Off":'sens 1',
                "Remove": 'sens 1',
                "MCU Stop Current": 'stop',
                "GSM Stop Current":'stop'
                }
    if clkButton in cmdDict.keys():
        cmd = cmdDict.get(clkButton)
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
            #ser.write('lcd 0'.encode('utf-8'))
            #data = ser.readline()
            #print(data)
        ser.close()
    
        buttonState(clkButton)
        
    except:
        messagebox.showerror("ERROR",'Please Check your portID or BaudRate')