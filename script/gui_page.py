class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width = 300
        self.height = 400
        myFrame = tk.Frame(self)
        myFrame.grid(row = 0, column = 2,padx=10,pady =10)
        #label = tk.Label(myFrame, text="TEST BUZZER", font=LARGE_FONT)
        #label.grid(row = 0, column = 0,pady=10,padx=10)
        myFrame2 = tk.Frame(self, width = 300, height = 400)
        myFrame2.grid(row = 3, column = 2,padx=10,pady =10)

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        button1.config(width =10)
        button1.grid(row = 3, column = 4)

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageTwo))
        button2.config(width =10)
        button2.grid(row =3, column = 5)
        
        button3 = tk.Button(self, text = "BUZZER TEST")
        
        button3.config(width = 15, command = lambda button = button3:serialConnect(button, portid, baud))
        button3.grid(row =1, column =2)
        button4 = tk.Button(myFrame2,text ="BUZ-PASS")
        button4.config(width = 15, )
        button4.grid(row =2, column =2)

        button5 = tk.Button(myFrame2,text = "BUZ-FAIL")
        button5.config(width =15)
        button5.grid(row = 2, column = 3)
        myCanvas = tk.Text(myFrame, bg="white",width =50)
        myCanvas.grid(row=1, column =3)


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



class PageThree(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width = 300
        self.height = 400
        myFrame = tk.Frame(self)
        myFrame.grid(row = 0, column = 2,padx=10,pady =10)
        myFrame2 = tk.Frame(self, width = 300, height = 400)
        myFrame2.grid(row = 3, column = 2,padx=10,pady =10)

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageTwo))
        button1.config(width =10)
        button1.grid(row = 3, column = 4)

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(PageFour))
        button2.config(width =10)
        button2.grid(row =3, column = 5)
        
        button3 = tk.Button(self, text = "DISPLAY LED TEST")
        button3.config(width = 15,command = lambda button = button3:serialConnect(button, portid, baud)) 
        button3.grid(row =1, column =2)
        button4 = tk.Button(myFrame2,text ="DISPAY-PASS")
        button4.config(width = 15)
        button4.grid(row =2, column =2)

        button5 = tk.Button(myFrame2,text = "DISPLAY-FAIL")
        button5.config(width =15)
        button5.grid(row = 2, column = 3)
        myCanvas = tk.Text(myFrame, bg="white",width =50)
        myCanvas.grid(row=1, column =3)


class PageFour(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.width = 300
        self.height = 400
        myFrame = tk.Frame(self)
        myFrame.grid(row = 0, column = 2,padx=10,pady =10)
        myFrame2 = tk.Frame(self, width = 300, height = 400)
        myFrame2.grid(row = 3, column = 2,padx=10,pady =10)

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageThree))
        button1.config(width =10)
        button1.grid(row = 3, column = 4)

        button2 = tk.Button(self, text="Next",
                            command=lambda: controller.show_frame(StartPage))
        button2.config(width =10)
        button2.grid(row =3, column = 5)
        
        button3 = tk.Button(self, text = "VALVE TEST")
        button3.config(width = 15)
        button3.grid(row =1, column =2)
        button4 = tk.Button(myFrame2,text ="VALVE-PASS")
        button4.config(width = 15)
        button4.grid(row =2, column =2)

        button5 = tk.Button(myFrame2,text = "VALVE-FAIL")
        button5.config(width =15)
        button5.grid(row = 2, column = 3)
        myCanvas = tk.Text(myFrame, bg="white",width =50)
        myCanvas.grid(row=1, column =3)
