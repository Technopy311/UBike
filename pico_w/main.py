from time import sleep
from machine import Pin
import _thread
import mfrc522
from robust_connection import send_uuid, connect_wifi
from rgb import RGB

#Checkeos iniciales
reader = mfrc522.MFRC522()
rgb = RGB() 
buzzer = Pin(, Pin.OUT)

#loop principal
def main()