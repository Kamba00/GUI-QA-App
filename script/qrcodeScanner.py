import cv2
import time
from pyzbar import pyzbar

def qrscan():
    with open("Qrcode_result.txt", mode ='r') as file:
                x =file.read()
                print(x)



""" def read_qrcodes(frame):
    qrcodes = pyzbar.decode(frame)
    for qrcode in qrcodes:
        x,y,w,h = qrcode.rect
        #read qrcode and decode info
        qrcode_info = qrcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        #add text from qr code       
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, qrcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        with open("Qrcode_result.txt", mode ='w') as file:
            file.write( qrcode_info)
    return frame

def qrscan():
    #open camera port
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #scan qrcode & loop until user inputs ESC button to cancel
    while ret:
        ret, frame = camera.read()
        frame = read_qrcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

        

    #Release camera clear all windows 
    camera.release()
    cv2.destroyAllWindows()
 """