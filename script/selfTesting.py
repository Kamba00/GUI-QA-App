###################################################################################################
# Step 1 : Setup initial basic graphics
# Step 2: Update available COMs & Baude rate
# Step 3: Serial connection setup
# Step 4: Dynamic GUI update
# Step 5: Testing & Debugging
###################################################################################################

from tkinter import *
import serial.tools.list_ports
import threading
import signal
import time

LARGE_FONT= ("Comic Sans MS", 18)
MEDIUM_FONT = ("Comic Sans MS", 11)
MEDIUM_BT = ("Merge Pro", 10, 'bold')
SMALL_FONT = ("Merge Pro", 10)


def signal_handler(signum, frame):
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


class PageOne:
    
    def __init__(self, master):
        frame = Frame(master)
        frame.grid(row = 4, column=0)
        self.width = 300
        self.height = 400
        #frame for the textbox
        frame1 = Frame(self, highlightthickness=2)
        frame1.grid(row=0, column =0, padx =10, pady= 10, sticky = 'NSEW')
        test_label =Label(frame1, text="CSM Self Test \n Automatic Testing of PCBA Sub System",font = MEDIUM_FONT, foreground= '#021E3C')
        test_label.grid(column=0, row=0, pady=10, padx=10, sticky = 'N')
        #textbox for entering the information to user
        #inputText = tk.Text(frame1,width = 40, height = 30, font = SMALL_FONT)
        #inputText.insert(1.0, "CSM SELF TEST IN PROGRESS . . . .\n", )
        #inputText.grid(row =0, column =1, padx =10, pady =10)
        #button for next page for user interface test like buzzer 
        cont_but = Button(self, text="CONTINUE", bg="white", width = 15,state ='disabled' )
        cont_but.config(background="#add8e6", foreground = 'white')
        cont_but.grid(row = 1, column =0, padx =10, pady = 20)
        self.myCanvas= Canvas(frame1, width =300,height = 500, bg ="white")
        self.myCanvas.create_text(100,10,fill="grey",font=MEDIUM_FONT,
                        text="")
        self.myCanvas.grid(row =0, column =1)
        self_but = Button(frame1, text="SELF-TEST", bg="white", width = 15 )
        self_but.config(background="#add8e6", foreground = 'white', command= lambda:self.text_update())
        self_but.grid(row =2, column =0)


    def text_update(self):
        static_test = "CSM TEST IN PROGRESS"
        test_string = "......"
        canvas_text = self.myCanvas.create_text(50, 10, text="", anchor=NW)
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


def atCommand():
    #mapping of the cli commands and parsing the commands thru serial port"
    global ser
    cmd = "AT+TSELF"
    cmd = cmd +'\r\n'
    if ser.in_waiting == 0:
        ser.write(cmd.encode('utf-8'))
        time.sleep(0.2)
        print("command done")





class Graphics():
    pass


def connect_menu_init():
    global root, connect_btn, refresh_btn, graph
    root = Tk()
    root.title("Serial communication")
    root.geometry("500x500")
    root.config(bg="white")

    port_lable = Label(root, text="Available Port(s): ", bg="white")
    port_lable.grid(column=1, row=2, pady=20, padx=10)

    port_bd = Label(root, text="Baude Rate: ", bg="white")
    port_bd.grid(column=1, row=3, pady=20, padx=10)

    refresh_btn = Button(root, text="R", height=2,
                         width=10, command=update_coms)
    refresh_btn.grid(column=3, row=2)

    connect_btn = Button(root, text="Connect", height=2,
                         width=10, state="disabled", command=connexion)
    connect_btn.grid(column=3, row=4)
    baud_select()
    update_coms()
    at_btn = Button(root, text=" AT Command", height=2,
                         width=10, state="active", command=atCommand)
    at_btn.grid(column=3, row=5)

    graph = Graphics()
    graph.canvas = Canvas(root, width=300, height=300,
                          bg="white", highlightthickness=0)
    graph.canvas.grid(row=5, columnspan=5)

 
    # Dynamic update
    graph.text = graph.canvas.create_text(
        150, 150, anchor=E, font=("Helvetica", "10"), text="---------------------------")




def connect_check(args):
    if "-" in clicked_com.get() or "-" in clicked_bd.get():
        connect_btn["state"] = "disable"
    else:
        connect_btn["state"] = "active"


def baud_select():
    global clicked_bd, drop_bd
    clicked_bd = StringVar()
    bds = ["-",
           "300",
           "600",
           "1200",
           "2400",
           "4800",
           "9600",
           "14400",
           "19200",
           "28800",
           "38400",
           "56000",
           "57600",
           "115200",
           "128000",
           "256000"]
    clicked_bd.set(bds[0])
    drop_bd = OptionMenu(root, clicked_bd, *bds, command=connect_check)
    drop_bd.config(width=20)
    drop_bd.grid(column=2, row=3, padx=50)


def update_coms():
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
    drop_COM = OptionMenu(root, clicked_com, *coms, command=connect_check)
    drop_COM.config(width=20)
    drop_COM.grid(column=2, row=2, padx=50)
    connect_check(0)


def graph_control(graph):
    cmdDict = {'+TSELF:0,0':'Int OSC: Fail','+TSELF:1,1':'External OSC: Pass',
                '+TSELF:5,1':'ACC: Pass', '+TSELF:6,1': 'NFC: Pass'
                }
    print(graph.output)
    text = graph.output.rstrip()
    if text in cmdDict.keys():
        print("match")
        graph.output = cmdDict.get(text)
    else:
        print("no match")
    graph.canvas.itemconfig(
        graph.text, text=f"{graph.output}")


def readSerial():
    print("thread start")
    line = []
    global serialData, graph
    while serialData :
        data = ser.readline()
        if len(data) > 0:
            try:
                data_sensor = data.decode('utf8')
                time.sleep(1)
                line.append(data_sensor.rstrip())
                graph.output = data_sensor
                print(line)
                t2 = threading.Thread(target=graph_control, args=(graph,))
                t2.deamon = True
                t2.start()

            except:
                pass


def connexion():
    global ser, serialData
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
        port = clicked_com.get()
        baud = clicked_bd.get()
        try:
            ser = serial.Serial(port, baud, timeout=0)
        except:
            pass
        t1 = threading.Thread(target=readSerial)
        t1.deamon = True
        t1.start()


def close_window():
    global root, serialData
    serialData = False
    root.destroy()


connect_menu_init()
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()