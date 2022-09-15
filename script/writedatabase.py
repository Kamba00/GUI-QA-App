import sqlite3
import sys
import time
import datetime
import traceback
import csv
conn = sqlite3.connect('csmsystemCheck.db')
c =conn.cursor()
unix = int(time.time())
dateStamp = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
def data_entry(resultentry):
    try:
        sql_insert = """INSERT INTO systemCheck VALUES(
                        :unix,
                        :dateStamp,
                        :msn_num,
                        :gasbody_num,
                        :pcb_num,
                        :reg_num,
                        :mcurrent,
                        :gcurrent,
                        :Amode,
                        :Buz,
                        :Display,
                        :GasOn,
                        :LED,
                        :NFC,
                        :Lock_Reg,
                        :Remov,
                        :SelfTest,
                        :UIButton,
                        :Unlock_Reg,
                        :ValvClose,
                        :ValvOpen,
                        :QA)"""
        resultentry.insert(0, unix)
        resultentry.insert(1, dateStamp)
        print(len(resultentry))
        c.execute(sql_insert,resultentry)
        conn.commit()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    conn.close()

    """ with open("QAresult.txt", mode ='w') as file:
            for value in resultentry:
                file.writerows(value) """

