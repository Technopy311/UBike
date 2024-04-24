from time import sleep
from machine import Pin, Timer
import _thread
import mfrc522
import queue
from robust_connection import send_uuid, connect_wifi
from rgb import RGB

#Checkeos iniciales
status = queue.Queue()
'''
Estados del módulo (Para debug y comunicacion entre hilos) - Respectivo color:
------------------
0 = Iniciando - Blanco
1 = Neutro y desocupado (Listo para leer, se autentica con cualquier tarjeta autorizada y establecida como sin uso actual en el registro) - Verde
2 = Neutro y ocupado (Listo para leer, solo la tarjeta del usuario actual desbloqueará el seguro) - Magenta
3 = Leyendo etiqueta - Amarillo
4 = Comunicando / Autenticando - Amarillo
5 = Aceptado / Solenoide abierto - Azul
-1 = Error / Estado de emergencia - Rojo
'''
reader = mfrc522.MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0) #Reservar estos pines para el lector RFID
url = "http://192.168.100.163:8080/picow"
reader.init()
rgb = RGB(7, 8, 9) 
rgb.setColor("white")
relay = Pin(5, Pin.OUT)
buzzer = Pin(6, Pin.OUT)
#loop principal (Thread 0)
def main():
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        send_uid = reader.
    
#loop secundario(Thread 1)
def second():
    #Comprueba conexión con la terminal cada cierto tiempo, si no es correcta, se entra en modo emergencia
    while True:
        sleep(10)
    
#Inicia loop secundario
_thread.start_new_thread(second, ())

while True:
    main()