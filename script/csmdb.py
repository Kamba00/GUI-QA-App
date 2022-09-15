import sqlite3
conn = sqlite3.connect('csmsystemCheck.db')
c =conn.cursor()
c.execute("""CREATE TABLE systemCheck(
                    unix INT,
                    dateStamp TEXT,
                    msn_num VAR PRIMARY KEY,
                    gasbody_num VAR,
                    pcb_num VAR,
                    reg_num VAR,
                    mcurrent FLOAT,
                    gcurrent FLOAT,
                    Amode TEXT,
                    Buz TEXT,
                    Display TEXT,
                    GasOn TEXT,
                    LED  TEXT,
                    NFC TEXT,
                    Lock_Reg TEXT,
                    Remov TEXT,
                    SelfTest TEXT,
                    UIButton TEXT,
                    Unlock_Reg TEXT,
                    ValvClose TEXT,
                    ValvOpen TEXT,
                    QA TEXT) """)

conn.commit()
conn.close()


