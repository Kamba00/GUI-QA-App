from os import close, system as sys
import signal
import threading
from tkinter import *
from tkinter import ttk
import re
import time
import serial
import serial.tools.list_ports
import sqlite3
from tkinter import messagebox
from writedatabase import *
sqlite3.paramstyle = 'named'

result =[]
TEST_NUMBER = 19
qa_result = ""

def signal_handler(signum, frame):
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)




def csmcheck_menu_init():
    global root, graph, msc_entry, gsc_entry
    root = Tk()
    root.title("CSM System Check")
    root.geometry("925x700")
    root.config(bg="light blue")
    root.option_add("*Font", "Montserrat 10")
    msc_val = StringVar()
    gsc_val = StringVar()
    
    portbaudInput()
    partNumbers()

    msc_button = Button(root, text="MCU Stop Current: ", bg="white")
    msc_button.config(command = lambda button =msc_button:writeCmd(button))
    msc_button.grid(column=4, row=6, pady=20, padx=10)
    msc_entry = Entry(root, textvariable = msc_val, font=('calibre',10,'normal'))
    msc_entry.grid(column =5, row =6)

    gsc_button = Button(root, text="GSM Stop Current: ", bg="white")
    msc_button.config(command = lambda button =msc_button:writeCmd(button))
    gsc_button.grid(column=4, row=7, pady=20, padx=10)
    gsc_entry = Entry(root, textvariable = gsc_val, font=('calibre',10,'normal'))
    gsc_entry.grid(column =5, row =7)

    cancel_btn_Pass = Button(root, text="Cancel", height=1,width=10,foreground='red', command = cancelsys)
    cancel_btn_Pass.grid(column=4, row=12)
    save_btn_Pass = Button(root, text="Save", height=1,width=10, state="active",foreground='green', command = submit)
    save_btn_Pass.grid(column=5, row=12)
    
    
    
    userPassFail()

    baudrate_select()
    comport_update()



def portbaudInput():
    global connect_btn, refresh_btn
    port_label = Label(root, text="Available Port(s): ", bg="white")
    port_label.grid(column=0, row=0, pady=20, padx=10)

    port_bd = Label(root, text="Baude Rate: ", bg="white")
    port_bd.grid(column=0, row=1, pady=20, padx=10)

    refresh_btn = Button(root, text="Refresh", height=1,width=10, command=comport_update)
    refresh_btn.grid(column=2, row=0)

    connect_btn = Button(root, text="Connect", height=1,width=10, state="disabled", command=connect_serial)
    connect_btn.grid(column=2, row=1)



def userPassFail():
    global buzzer_btn_Pass, led_btn_Pass,Display_btn_Pass,shutoff1_btn_Pass,gas_on_btn_Pass
    global shutoff2_btn_Pass,remove_btn_Pass,lock_btn_Pass,unlock_btn_Pass,gsm_btn_Pass
    global  selfTest_btn_Pass,amode_btn_Pass,ui_btn_Pass, nfc_btn_Pass
    global mode_var, mode
    #Buttons to run the CLI commands and also get input for user for test pass/fail
    buzzer = Button(root, text="Buzzer", bg="white", height = 1, width = 10, state = "active")
    buzzer.config(command = lambda button =buzzer:writeCmd(button))
    buzzer.grid(column=0, row=6, pady=20, padx=10, sticky = NE)
    buzzer_btn_Pass = Button(root, text="Buz-Pass", height=1,width=10, state="disabled",foreground='green')
    buzzer_btn_Pass.config(command = lambda button =buzzer_btn_Pass:collectResult(button))
    buzzer_btn_Pass.grid(column=1, row=6)

    led = Button(root, text="LED", bg="white")
    led.config(command = lambda button =led:writeCmd(button))
    led.grid(column=0, row=7, pady=20, padx=10, sticky = NE)
    led_btn_Pass = Button(root, text="LED-Pass", height=1,width=10, state="disabled",foreground='green', command=connect_serial)
    led_btn_Pass.config(command = lambda button =led_btn_Pass:collectResult(button))
    led_btn_Pass.grid(column=1, row=7)
    

    display= Button(root, text="Display", bg="white")
    display.config(command = lambda button =display:writeCmd(button))
    display.grid(column=0, row=8, pady=20, padx=10, sticky = NE)
    Display_btn_Pass = Button(root, text="Display-Pass", height=1,width=10, state="disabled",foreground='green', command=connect_serial)
    Display_btn_Pass.config(command = lambda button =Display_btn_Pass:collectResult(button))
    Display_btn_Pass.grid(column=1, row= 8)

    shutoff1 = Button(root, text="Valve-Open", bg="white")
    shutoff1.config(command = lambda button =shutoff1:writeCmd(button))
    shutoff1.grid(column=0, row=9, pady=20, padx=10, sticky = NE)
    shutoff1_btn_Pass = Button(root, text="Valve Open-Pass", height=1,width=14, state="disabled",foreground='green')
    shutoff1_btn_Pass.config(command = lambda button =shutoff1_btn_Pass:collectResult(button))
    shutoff1_btn_Pass.grid(column=1, row=9)
    
    shutoff2 = Button(root, text="Valve-Close", bg="white")
    shutoff2.config(command = lambda button =shutoff2:writeCmd(button))
    shutoff2.grid(column=0, row=10, pady=20, padx=10, sticky = NE)
    shutoff2_btn_Pass = Button(root, text="Valve Close-Pass", height=1,width=14, state="disabled",foreground='green')
    shutoff2_btn_Pass.config(command = lambda button =shutoff2_btn_Pass:collectResult(button))
    shutoff2_btn_Pass.grid(column=1, row=10)

    gas_on = Button(root, text="Gas-On", bg="white")
    gas_on.config(command = lambda button =gas_on:writeCmd(button))
    gas_on.grid(column=0, row=11, pady=20, padx=10, sticky = NE)
    gas_on_btn_Pass = Button(root, text="GasOn-Pass", height=1,width=14, state="disabled",foreground='green')
    gas_on_btn_Pass.config(command = lambda button =gas_on_btn_Pass:collectResult(button))
    gas_on_btn_Pass.grid(column=1, row=11)
    
    remove = Button(root, text="Remove", bg="white")
    remove.config(command = lambda button =remove:writeCmd(button))
    remove.grid(column=0, row=12, pady=20, padx=10, sticky = NE)
    remove_btn_Pass = Button(root, text="Remove-Pass", height=1,width=10, state="disabled",foreground='green')
    remove_btn_Pass.config(command = lambda button =remove_btn_Pass:collectResult(button))
    remove_btn_Pass.grid(column=1, row=12)

    lock = Button(root, text="Regulator Lock", bg="white")
    lock.config(command = lambda button =lock:writeCmd(button))
    lock.grid(column=2, row=7, pady=20, padx=10, sticky = NE)
    lock_btn_Pass = Button(root, text="Lock-Pass", height=1,width=12, state="disabled",foreground='green')
    lock_btn_Pass.config(command = lambda button =lock_btn_Pass:collectResult(button))
    lock_btn_Pass.grid(column=3, row=7)

    unlock = Button(root, text="UnLock", bg="white")
    unlock.config(command = lambda button =unlock:writeCmd(button))
    unlock.grid(column=2, row=6, pady=20, padx=10, sticky = NE)
    unlock_btn_Pass = Button(root, text="Unlock-Pass", height=1,width=12, state="disabled",foreground='green')
    unlock_btn_Pass.config(command = lambda button =unlock_btn_Pass:collectResult(button))
    unlock_btn_Pass.grid(column=3, row=6)

    mode_var = StringVar()
    mode_option = [0, 1, 2]
    mode_var.set(mode_option[0])
    mode = Button(root, text=" Change Mode", bg="white", state = "disabled")
    mode.grid(column=3, row=0, pady=20, padx=10, sticky = NE,)
    mode.config(command = lambda button =mode:setMode())
    mode_btn = OptionMenu(root, mode_var, *mode_option)
    #mode_btn.config(command = lambda button =mode_btn:setMode(button))
    mode_btn.grid(column=4, row=0)

    selfTest = Button(root, text="Self Test", bg="white")
    selfTest.config(command = lambda button =selfTest:writeCmd(button))
    selfTest.grid(column=2, row=8, pady=20, padx=10, sticky = NE)
    selfTest_btn_Pass = Button(root, text="SelfTest-Pass", height=1,width=12, state="disabled",foreground='green')
    selfTest_btn_Pass.config(command = lambda button =selfTest_btn_Pass:collectResult(button))
    selfTest_btn_Pass.grid(column=3, row=8)
 
    amode = Button(root, text="Active Mode", bg="white")
    amode.config(command = lambda button =amode:writeCmd(button))
    amode.grid(column=2, row=9, pady=20, padx=10, sticky =NE)
    amode_btn_Pass = Button(root, text="AM-Pass", height=1,width=12, state="disabled",foreground='green')
    amode_btn_Pass.config(command = lambda button =amode_btn_Pass:collectResult(button))
    amode_btn_Pass.grid(column=3, row=9, pady=20, padx=10)

    #ui = Label(root, text="UI Button", bg="white")
    #ui.config(command = lambda button = ui:writeCmd(button))
    #ui.grid(column=2, row=10, pady=20, padx=10, sticky = NE)
    ui_btn_Pass = Button(root, text="UI Button-Pass", height=1,width=12, state="disabled",foreground='green')
    ui_btn_Pass.grid(column=3,row=10)
    ui_btn_Pass.config(command = lambda button =ui_btn_Pass:collectResult(button))
 
    #nfc= Label(root, text="NFC", bg="white")
    #nfc.grid(column=2, row=11, pady=20, padx=10, sticky = NE)
    nfc_btn_Pass = Button(root, text="NFC-Pass", height=1,width=12, state="disabled",foreground='green')
    nfc_btn_Pass.grid(column=3, row=11)
    nfc_btn_Pass.config(command = lambda button =nfc_btn_Pass:collectResult(button))

def setMode():
    mode_num = mode_var.get()
    mode_num = 'Mode ' + mode_num 
    serialConnect(mode_num)


def partNumbers():
    global msn, gasbody, pcb, regulator, outputUserinfo
    global msn_entry, gasbody_entry,msn, gasbody, gasbody_entry, pcb_entry, regulator_entry
    frame1 = Frame(root, height = 200,width = 200, highlightthickness=3)
    name_var = StringVar()
    gasbody_qr = StringVar()
    pcb_qr = StringVar()
    reg_qr= StringVar()
    msn = Button(root, text="MSN", bg="white", state = "disabled")
    msn.config(command = lambda button =msn:getQr(button))
    msn.grid(column=3, row=1, pady=20, padx=15)
    msn_entry = Entry(root, textvariable = name_var, font=('calibre',10,'normal'))
    msn_entry.grid(column =4, row =1)

    gasbody = Button(root, text="GasBody", bg="white", state = 'disabled')
    gasbody.config(command = lambda button =gasbody:getQr(button))
    gasbody.grid(column=0, row=4, pady=20, padx=10)
    gasbody_entry = Entry(root, textvariable = gasbody_qr, font=('calibre',10,'normal'))
    gasbody_entry.grid(column =1, row =4)

    pcb = Button(root, text="PCBA", bg="white", state = 'disabled')
    pcb.config(command = lambda button =pcb:getQr(button))
    pcb.grid(column=2, row=4, pady=20, padx=10)
    pcb_entry = Entry(root, textvariable = pcb_qr, font=('calibre',10,'normal'))
    pcb_entry.grid(column =3, row =4)
    
    regulator = Button(root, text="Regulator", bg="white", state = 'disabled')
    regulator.config(command = lambda button =regulator:getQr(button))
    regulator.grid(column=4, row=4, pady=20, padx=10)
    regulator_entry = Entry(root, textvariable = reg_qr, font=('calibre',10,'normal'))
    regulator_entry.grid(column =5, row =4)
    #frame1.grid(column=5,row=9)
    outputUserinfo =Text(root, height = 15,width =40)
    outputUserinfo.grid(column=4, row =8, rowspan=4, columnspan=2)



def cancelsys():
    root.quit()
    

def buttonState(args):
    print(args)
    stateDict = {'Buzzer': buzzer_btn_Pass, 'LED': led_btn_Pass,
                'Display': Display_btn_Pass,"Valve-Open": shutoff1_btn_Pass,
                "Gas-On": gas_on_btn_Pass, "Valve-Close": shutoff2_btn_Pass,  "Remove": remove_btn_Pass,
                "Regulator Lock":lock_btn_Pass, "UnLock": unlock_btn_Pass,
                "Self Test": selfTest_btn_Pass,
                "Active Mode":amode_btn_Pass,"UI Button":ui_btn_Pass}
    
    try:
        stateDict.get(args)['state']= 'active'
    except:
        messagebox("No test done")


def connection_check(args):
    if "-" in clicked_com.get() or "-" in clicked_bd.get():
        connect_btn["state"] = "disable"
    else:
        connect_btn["state"] = "active"

def baudrate_select():
    global clicked_bd, drop_bd
    clicked_bd = StringVar()
    bds = ["-", "9600", "115200", "921600"]
    clicked_bd.set(bds[0])
    drop_bd = OptionMenu(root, clicked_bd, *bds, command=connection_check)
    drop_bd.config(width=10)
    drop_bd.grid(column=1, row=1, padx=50)



def comport_update():
    global clicked_com, drop_COM
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    try:
        drop_COM.destroy()
    except:
        pass
    clicked_com = StringVar()
    clicked_com.set(coms[0])
    drop_COM =OptionMenu(root, clicked_com, *coms, command = connection_check)
    drop_COM.config(width=10)
    drop_COM.grid(column=1, row=0, padx=50)
    connection_check(0)


def connect_serial():
    cmd = 'mode 0'+ '\r\n'
    global ser, serialData, portid, baud
    if connect_btn["text"] in "Disconnect":
        serialData = False
        connect_btn["text"] = "Connect"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_COM["state"] = "active"


    else:
        serialData = True
        connect_btn["text"] = "Disconnect"
        refresh_btn["state"] = "disable"
        drop_bd["state"] = "disable"
        drop_COM["state"] = "disable"
        mode["state"] = 'active'
        portid = clicked_com.get()
        print(portid)
        baud = clicked_bd.get()
        print(baud)
        try:
            ser= serial.Serial(portid, baud, timeout=0)
            ser.write(cmd.encode('utf-8'))
            time.sleep(0.1)
            messagebox.showinfo("Info","Meter Connected in Test Mode")
            ser.close()
        except:
            messagebox.showerror("Connection not obtained")
            pass
    #t1 = threading.Thread(target=serialRead)
    #t1.deamon = True
    #t1.start() 


def serialRead():
    print("thread start")
    global serialData
    ser = serial.Serial(portid, baud,timeout =0)
    if ser.isOpen():
        print('open')
    while serialData:
        data = ser.readline()
        print(data)
        if len(data) > 0:
            try:
                sensor = (data.decode('utf8'))
                data_sensor = (data.decode('utf8'))
                print(data_sensor)
                ser.close()
            except:
                pass
    

def writeCmd(args):
    #recieving the pressed button id and passing the button text to mapped CLI
    cmd = args.cget(('text'))
    print("clickedButton", cmd)
    #avialable commands can be changed to dictionary
    clicked_Button = ['Buzzer', 'LED', 'Display', "Valve-Open","Valve-Close",
                       "Regulator Lock","UnLock","GSM","Self Test","Active Mode", 
                       "Gas-On", "Gas-Off", "Remove", "MCU Stop Current", "GSM Stop Current"]
    try:
        if cmd in clicked_Button:
            #print("Pressed Button: ",cmd)
           serialConnect(cmd)
    except:
          messagebox.showerror("Error", 'Pressed Wrong Button')

def serialConnect(args):
    #mapping of the cli commands and parsing the commands thru serial port"
    #outputUserinfo.delete(1.0, END)
    clkButton = args
    lines =[]
    wait_time = 0.1
    print (clkButton)
    cmdDict = {'Buzzer':'buz 2', 'LED':'led 1', 'Display':'lcd 1',"Valve-Open": 'valve 1',
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
            #ser.write('lcd 0'.encode('utf-8'))
            #data = ser.readline()
            #print(data) 
        while True:
            line = ser.readline()
            lines.append(line.decode('utf-8').rstrip())

        # wait for new data after each line
            timeout = time.time() + wait_time
            while not ser.inWaiting() and timeout > time.time():
                pass
            if not ser.inWaiting():
                break

        ser.close()
        print(lines)
        outputUserinfo.delete(1.0, END)
        for item in lines:
            user_info = item.replace(" ","")
            outputUserinfo.insert(1.0, user_info +"\n")
        if clkButton != 'Mode 1'and clkButton != 'Mode 2':
            buttonState(clkButton)
        else:
            pass
    except:
        messagebox.showerror("ERROR",'Please Check your portID or BaudRate')
    

def collectResult(args):
    #collecting result from the user input for QA pass
    passButton = args.cget(('text'))
    if passButton == "AM-Pass":
            ui_btn_Pass['state']= 'active'
    elif passButton == "UI Button-Pass":
        nfc_btn_Pass['state'] ='active'
    
    if not passButton in result:
        result.append(passButton)
    else:
        pass

    print (result)


def checkResult():
    """checking the length of User input of QA. setting the test number
        and check if all test is complete"""
    global allresults
    test_no = len(allresults)
    if test_no != TEST_NUMBER:
        messagebox.showwarning("CSM-QA","QA Incomplete or Has any QA Failed?")
        diff = (TEST_NUMBER-test_no)
        for i in range(diff):
            allresults.append("NULL")
            print(len(allresults))
            print(allresults)
        return False
    else:
        return True




def submit():
    #get entries from the entry items
    global allresults, qa_result
    try:
        msc_num = float(msc_entry.get())
        gsc_num = float(gsc_entry.get())
        #add the enteries to a list 
        res = [msn_entry.get(),gasbody_entry.get(),pcb_entry.get(), regulator_entry.get(),msc_num, 
                gsc_num]
    except:
        messagebox.showwarning("Error", "Wrong/Empyt Part numbers! Please check" )
    #sort the result list in alphabet for sql database entry
    result.sort() 
    allresults = res + result 
    qa_result = ""
    #check if the current is above the threshold, QA check!
    if msc_num > 60.0 or gsc_num >20.0:
        qa_result = "QA-Fail"
        messagebox.showwarning("QA Info", 'Current exceeds Limit')


    if checkResult() and qa_result == "":
        qa_result = 'QA-Pass'
        allresults.insert(len(allresults), qa_result)
        #input to sqltable
        data_entry(allresults)
        messagebox.showinfo("QA Result", "Saving to CSM SYSTEM CHECK DATABASE- {}".format (qa_result))
    elif checkResult() and qa_result != "":
        allresults.insert(len(allresults), qa_result)
        #input to sqltable
        data_entry(allresults)
        messagebox.showinfo("QA RESULT", "Saving to CSM SYSTEM CHECK DATABASE- {}".format (qa_result))
    elif not checkResult() or qa_result == "":
        print("YES")
        qa_result = "QA-Fail"
        allresults.insert(len(allresults), qa_result)
        #input to sqltable
        data_entry(allresults)
        messagebox.showinfo("QA RESULT", "Saving to CSM SYSTEM CHECK DATABASE- {}".format (qa_result))
 

    

def close_window():
    global root
    serialData = False
    root.destroy()

csmcheck_menu_init()
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()

