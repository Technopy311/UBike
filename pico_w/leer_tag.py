from mfrc522 import MFRC522
from time import sleep	

from robust_connection import send_uuid, connect_wifi

lector = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

print("Lector activo...\n")

url = "http://192.168.100.163:8080/picow"

while True:
    lector.init()
    (stat, tag_type) = lector.request(lector.REQIDL)
    if stat == lector.OK:
        (stat, uid) = lector.SelectTagSN()
        if stat == lector.OK:
            identificador = int.from_bytes(bytes(uid),"little",False)
            #identificador = str(identificador)
            print("UID: "+str(identificador))
            
            send_uuid(url, identificador)
        
            
sleep(1)
