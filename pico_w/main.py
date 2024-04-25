from time import sleep
from machine import Pin, Timer
import _thread
import mfrc522
import queue
from robust_connection import send_uuid, connect_wifi
from rgb import RGB

# Initial Checks
status = queue.Queue()

'''
Module Status (For debugging and Thread between communication) - Repective color:
0 = Booting - White
1 = Neutral and not busy - Green
2 = Neutral and busy - Magenta
3 = Reading label - Yellow
4 = Communicating / Authenticating - Yellow
5 = Accepted / Open solenoid - Blue
-1 = Error / Emergency status - Red

'''

reader = mfrc522.MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0) #Reserve these pins for RFID module
url = "http://192.168.100.163:8080/picow"
reader.init()
rgb = RGB(7, 8, 9) 
rgb.setColor("white")
relay = Pin(5, Pin.OUT)
buzzer = Pin(6, Pin.OUT)
# Main thread (Thread 0)
def main():
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        send_uid = reader.
    
# Secondary thread (Thread 1)
def second():
    # Checks connection with the terminal each cearting time, if not correct, enters emergency mode
    while True:
        sleep(1*60) # 1 minute
    

# Starts secondary thread
_thread.start_new_thread(second, ())

while True:
    main()