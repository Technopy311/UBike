from time import sleep
from machine import Pin, Timer
import _thread
import mfrc522
from robust_connection import send_uuid, connect_wifi
from rgb import RGB

#Checkeos iniciales
reader = mfrc522.MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0) #Reservar estos pines para el lector
rgb = RGB() 
relay = Pin(, Pin.OUT)
buzzer = Pin(, Pin.OUT)
'''
Estados del módulo (Para debug y comunicacion entre hilos):
------------------
0 = Iniciando
1 = Neutro (Listo para leer)
2 = Leyendo etiqueta
3 = Comunicando / Autenticando
4 = Aceptado / Solenoide abierto
-1 = Error / Estado de emergencia
'''
status = 0

#loop principal (Thread 0)
def main():
    
#loop secundario(Thread 1)
def second():
    
#Inicia loop secundario
_thread.start_new_thread(second, ())
while True:
    main()