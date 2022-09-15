import tkinter as tk
from tkinter import Frame, PhotoImage, ttk
from tkinter.constants import NSEW, SEL_FIRST
import serial
import time
import serial.tools.list_ports
from tkinter import messagebox
import threading

LARGE_FONT= ("Comic Sans MS", 18)
MEDIUM_FONT = ("Comic Sans MS", 11)
MEDIUM_BT = ("Merge Pro", 10, 'bold')
SMALL_FONT = ("Merge Pro", 10)


class Graphics():
    pass


graph = Graphics()




def readSerail():
    print("thread start")
    lines =[]
    wait_time = 0.1
    if ser.isOpen():
        print('open')

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

def self_testing():
    #self test method AT protocol
    print("self testing in progress")




class CsmSystemCheck(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)
            frame.config(background='#021E3C', width = 600, height =500)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="CSM System Check ", font= LARGE_FONT,bg='#021E3C', foreground = 'white')
        label.grid(row = 0, column = 0, pady=5,padx=5)
        #move to next window for csm testing 
        button = tk.Button(self, text="START TEST",
                            command=lambda:controller.show_frame(PageOne))
        button.config(width = 15, font = MEDIUM_BT, background="light blue", foreground="white")
        button.grid(row = 8, column = 0, padx=10, pady=15)
        #take input from user for portid & baud rate
        self.portbaudInput()
        #options for different baud rate
        self.baudrate_select()
        #option to update baud rate and com port 
        self.comport_update()
        #Frames and widgets to get the serial number with QR scan
        self.partNumbers()
    

    def portbaudInput(self):
        #establish a serial connection with CSM meter
        global connect_btn, refresh_btn, first_frame
        first_frame = tk.Frame(self, highlightthickness=2)
        first_frame.grid(row = 1, column =0, padx =10, pady= 5)
        port_label = tk.Label(first_frame, text="Available Port(s): ", font = MEDIUM_FONT, foreground= '#021E3C')
        port_label.grid(column=0, row=1, pady=10, padx=10)

        port_bd = tk.Label(first_frame, text="Baude Rate: ",font = MEDIUM_FONT, foreground= '#021E3C')
        port_bd.grid(column=0, row=2, pady=10, padx=10)

        refresh_btn = tk.Button(first_frame, text="REFRESH", height=1,width=10, command=self.comport_update)
        refresh_btn.config(width = 15, font = MEDIUM_BT, background='dark grey', foreground="white")
        refresh_btn.grid(column=2, row=1)

        connect_btn = tk.Button(first_frame, text="CONNECT", height=1,width=10, state="disabled",  command=self.connect_serial)
        connect_btn.config(width = 15,font = MEDIUM_BT, background='dark grey', foreground='white', activebackground="green")
        connect_btn.grid(column=2, row=2)
    
    def baudrate_select(self):
        global clicked_bd, drop_bd
        clicked_bd = tk.StringVar()
        bds = ["-", "9600", "115200", "921600"]
        clicked_bd.set(bds[0])
        drop_bd = tk.OptionMenu(first_frame, clicked_bd, *bds, command=self.connection_check)
        drop_bd.config(width=15)
        drop_bd.grid(column=1, row=2, padx=10)
    
    def comport_update(self):
        global clicked_com, drop_COM
        ports = serial.tools.list_ports.comports()
        coms = [com[0] for com in ports]
        coms.insert(0, "-")
        try:
            drop_COM.destroy()
        except:
            pass
        clicked_com = tk.StringVar()
        clicked_com.set(coms[0])
        drop_COM =tk.OptionMenu(first_frame, clicked_com, *coms, command =self.connection_check)
        drop_COM.config(width=15)
        drop_COM.grid(column=1, row=1, padx=10)
        self.connection_check(0)
    
    def connection_check(self, args):
        if "-" in clicked_com.get() or "-" in clicked_bd.get():
            connect_btn["state"] = "disable"
        else:
            connect_btn["state"] = "active"

    def connect_serial(Self):
        cmd = 'mode 0'+ '\r\n'
        global ser, serialData, portid, baud
        if connect_btn["text"] in "Disconnect":
            serialData = False
            connect_btn["text"] = "CONNECT"
            connect_btn['foreground'] = 'white'
            refresh_btn["state"] = "active"
            drop_bd["state"] = "active"
            drop_COM["state"] = "active"
        else:
            serialData = True
            connect_btn["text"] = "Disconnect"
            connect_btn['background'] = 'green'
            refresh_btn["state"] = "disable"
            drop_bd["state"] = "disable"
            drop_COM["state"] = "disable"
            portid = clicked_com.get()
            print(portid)
            baud = clicked_bd.get()
            print(baud)
            try:
                ser= serial.Serial(portid, baud, timeout=0)
                ser.write(cmd.encode('utf-8'))
                time.sleep(0.1)
                messagebox.showinfo("Info","Meter Connected in Test Mode")
            except:
                pass
            t1 = threading.Thread(target=readSerial)
            t1.deamon = True
            t1.start()  


    def partNumbers(self):
            global msn, gasbody, pcb, regulator, outputUserinfo
            global msn_entry, gasbody_entry,msn, gasbody, gasbody_entry, pcb_entry, regulator_entry
            frame1 = tk.Frame(self, highlightthickness=2)
            frame1.grid(row=3, column =0, padx =10, pady= 10, sticky = 'NSEW')
            frame2 = tk.Frame(self, highlightthickness=2)
            frame2.grid(row=4, column =0, padx =10, pady= 5, sticky = 'NSEW')
            frame3 = tk.Frame(self, highlightthickness=2)
            frame3.grid(row=5, column =0, padx =10, pady= 5, sticky = 'NSEW')
            frame4 = tk.Frame(self, highlightthickness=2)
            frame4.grid(row=6, column =0, padx =10, pady= 5, sticky = 'NSEW')
            frame5 = tk.Frame(self, highlightthickness=2)
            frame5.grid(row=7, column =0, padx =10, pady= 5, sticky = 'NSEW')
            check_img = PhotoImage(file ='check_mark2.png') 
            #input variable for 
            name_var = tk.StringVar()
            gasbody_qr = tk.StringVar()
            pcb_qr = tk.StringVar()
            reg_qr= tk.StringVar()
            
            #image for check button 
            img_label = tk.Label(image = check_img)
            msn = tk.Label(frame1, text="MSN Serial Number \n Manufacturer Serial Number (ex:SAAXX0031)", font = MEDIUM_FONT, foreground= '#021E3C')
            msn.grid(column=0, row=2, pady=5, padx=10)
            msn_entry = tk.Entry(frame1, textvariable = name_var, font=('calibre',10,'normal'), width =23)
            msn_entry.grid(column =2, row =2, pady=10, padx=10)
            msn_check = tk.Button(frame1, text = "yes", command = lambda:self.frameEnable)
            msn_check.grid(column=1, row=2, pady=5, padx=10)
            #disable all children in frame1
            for child in frame1.winfo_children():
                child.configure(state='disable')
            gasbody = tk.Label(frame2, text="GasBody Serial Number \n Gas Body Serial Number (ex:PGDBXX0031)    ",font = MEDIUM_FONT,foreground=  '#021E3C')
            gasbody.grid(column=0, row=2, pady=10, padx=10)
            gasbody_entry = tk.Entry(frame2, textvariable = gasbody_qr, font=('calibre',10,'normal'), width =25)
            gasbody_entry.grid(column =2, row =2, pady =10, padx =10)
            gasbody_check = tk.Button(frame2, text = "yes")
            gasbody_check.grid(column=1, row=2, pady=5, padx=10)
            #disalbe all widget in frame2
            for child in frame2.winfo_children():
                child.configure(state='disable')
            pcb = tk.Label(frame3, text="PCBA Serial Number \n  PCBA Serial Number (ex:CSMMXX000031)  ",font = MEDIUM_FONT, foreground= '#021E3C')
            pcb.grid(column=0, row=2, pady=10, padx=10)
            pcb_entry = tk.Entry(frame3, textvariable = pcb_qr, font=('calibre',10,'normal'), width =25)
            pcb_entry.grid(column =2, row =2, padx=10,pady =5)
            pcb_check = tk.Button(frame3, text = "yes")
            pcb_check.grid(column=1, row=2, pady=5, padx=10)
            #disable all widget in frame 3
            for child in frame3.winfo_children():
                child.configure(state='disable')
            regulator = tk.Label(frame4, text="Regulator Serial Number \n Regulator Serial Number (ex:PRDBXX0031)  ",font = MEDIUM_FONT, foreground= '#021E3C')
            regulator.grid(column=0, row=2, pady=10, padx=10)
            regulator_entry = tk.Entry(frame4, textvariable = reg_qr, font=('calibre',10,'normal'), width =25)
            regulator_entry.grid(column =2, row =2, padx =10, pady =5)
            reg_check = tk.Button(frame4, text = "yes")
            reg_check.grid(column=1, row=2, pady=5, padx=10)
            #disable all widget in frame 4
            for child in frame4.winfo_children():
                child.configure(state='disable')
            sim = tk.Label(frame5, text="Sim Serial Number \n Sim Serial Number (ex:XXXXXXX0031)      ",
                            font = MEDIUM_FONT, foreground= '#021E3C')
            sim.grid(column=0, row=1, pady=10, padx=10)
            sim_entry = tk.Entry(frame5, textvariable = reg_qr, font=('calibre',10,'normal'), width =25)
            sim_entry.grid(column =2, row =1, padx =10, pady =5)
            sim_check = tk.Button(frame5, text = "yes")
            sim_check.grid(column=1, row=1, pady=5, padx=10)
            for child in frame5.winfo_children():
                child.configure(state='disable')

    def frameEnable(self):
        #check button input and enable next frame in order
        pass
    def connect_serial(Self):
        cmd = 'mode 0'+ '\r\n'
        global ser, serialData, portid, baud
        if connect_btn["text"] in "Disconnect":
            serialData = False
            connect_btn["text"] = "CONNECT"
            connect_btn['foreground'] = 'white'
            refresh_btn["state"] = "active"
            drop_bd["state"] = "active"
            drop_COM["state"] = "active"
        else:
            serialData = True
            connect_btn["text"] = "Disconnect"
            connect_btn['background'] = 'green'
            refresh_btn["state"] = "disable"
            drop_bd["state"] = "disable"
            drop_COM["state"] = "disable"
            portid = clicked_com.get()
            print(portid)
            baud = clicked_bd.get()
            print(baud)
            try:
                ser= serial.Serial(portid, baud, timeout=0)
                ser.write(cmd.encode('utf-8'))
                time.sleep(0.1)
                messagebox.showinfo("Info","Meter Connected in Test Mode")
            except:
                pass
            t1 = threading.Thread(target=readSerail)
            t1.deamon = True
            t1.start() 
    def currentInput(self):
            global msc_entry, gsc_entry
            msc_val = tk.StringVar()
            gsc_val = tk.StringVar()

            msc_button = tk.Button(self, text="MEASURE CURRENT", bg="white")
            #msc_button.config(command = lambda button =msc_button:writeCmd(button))
            msc_button.grid(column=3, row=4, pady=20, padx=10)
            msc_button = tk.Label(self, text="MCU CURRENT: ", bg="white")
            #msc_button.config(command = lambda button =msc_button:writeCmd(button))
            msc_button.grid(column=2, row=5, pady=20, padx=10)
            msc_entry = tk.Entry(self, textvariable = msc_val, font=('calibre',10,'normal'))
            msc_entry.grid(column =3, row =5, padx=10, pady=10)

            gsc_button = tk.Label(self, text="GSM CURRENT: ", bg="white")
            #msc_button.config(command = lambda button =msc_button:writeCmd(button))
            gsc_button.grid(column=2, row=6, pady=20, padx=10)
            gsc_entry = tk.Entry(self, textvariable = gsc_val, font=('calibre',10,'normal'))
            gsc_entry.grid(column =3, row =6, padx =10, pady=10)

    def partnumvalidate(self, controller):
        res = {'msn':[msn_entry.get(),'S', 14],'gasbody':[gasbody_entry.get(),'PG',13 ],
                'pcb':[pcb_entry.get(),'CS',12],'reg':[regulator_entry.get(),'PR',13]}

        print (res)
        isCorrect = False
        for num in res.values():
            print(len(num[0]))
            if (len(num[0]) == num[2]) and (num[0][0:2] == num[1]):
                isCorrect = True
            else:
                isCorrect = True
                messagebox.showerror("Error", 'Wrong Part Numbers. Please check')
                break
        if isCorrect:
            messagebox.showinfo("Info", "To Csm System Test")
            controller.show_frame(PageOne)


class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width = 300
        self.height = 400
        #frame for the textbox
        frame1 = tk.Frame(self, highlightthickness=2)
        frame1.grid(row=0, column =0, padx =10, pady= 10, sticky = 'NSEW')
        test_label =tk.Label(frame1, text="CSM Self Test \n Automatic Testing of PCBA Sub System",font = MEDIUM_FONT, foreground= '#021E3C')
        test_label.grid(column=0, row=0, pady=10, padx=10, sticky = 'N')
        #textbox for entering the information to user
        #inputText = tk.Text(frame1,width = 40, height = 30, font = SMALL_FONT)
        #inputText.insert(1.0, "CSM SELF TEST IN PROGRESS . . . .\n", )
        #inputText.grid(row =0, column =1, padx =10, pady =10)
        #button for next page for user interface test like buzzer 
        cont_but = tk.Button(self, text="CONTINUE", bg="white", width = 15,state ='disabled' )
        cont_but.config(background="#add8e6", foreground = 'white', command=lambda: controller.show_frame(PageTwo))
        cont_but.grid(row = 1, column =0, padx =10, pady = 20)
        self.myCanvas= tk.Canvas(frame1, width =300,height = 500, bg ="white")
        self.myCanvas.create_text(100,10,fill="grey",font=MEDIUM_FONT,
                        text="")
        self.myCanvas.grid(row =0, column =1)
        self_but = tk.Button(frame1, text="SELF-TEST", bg="white", width = 15 )
        self_but.config(background="#add8e6", foreground = 'white', command= lambda:self.text_update())
        self_but.grid(row =2, column =0)


    def text_update(self):
        self_testing()
        static_test = "CSM TEST IN PROGRESS"
        test_string = "......"
        canvas_text = self.myCanvas.create_text(50, 10, text="", anchor=tk.NW)
        #Time delay between chars, in milliseconds
        delta = 500 
        delay = 0
        for i in range(len(test_string) + 1):
            s = static_test+test_string[:i]
            update_text = lambda s=s: self.myCanvas.itemconfigure(canvas_text, text=s)
            self.myCanvas.after(delay, update_text)
            delay += delta
        
    def selfTest_result(self):
        pass




class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width = 300
        self.height = 400
        myFrame = tk.Frame(self)
        myFrame.grid(row = 0, column = 2,padx=10,pady =10)
        myFrame2 = tk.Frame(self, width = 300, height = 400)
        myFrame2.grid(row = 3, column = 2,padx=10,pady =10)

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageOne))
        button1.config(width =10)
        button1.grid(row = 3, column = 4)

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageThree))
        button2.config(width =10)
        button2.grid(row =3, column = 5)
        
        button3 = tk.Button(self, text = "BLUE LED TEST")
        button3.config(width = 15, command = lambda button = button3:serialConnect(button, portid, baud))
        button3.grid(row =1, column =2)
        button4 = tk.Button(myFrame2,text ="LED-PASS")
        button4.config(width = 15)
        button4.grid(row =2, column =2)

        button5 = tk.Button(myFrame2,text = "LED-FAIL")
        button5.config(width =15)
        button5.grid(row = 2, column = 3)
        myCanvas = tk.Text(myFrame, bg="white",width =50)
        myCanvas.grid(row=1, column =3)








app = CsmSystemCheck()
app.title('CSM System Check')
app.iconbitmap('paygo_ico.ico')
app.mainloop() 













