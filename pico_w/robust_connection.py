import time
import network
import urequests as requests

from machine import Pin

ssid = 'FPWOM'
password = 'NHl7g371#0'

led = Pin(13, Pin.OUT)

led.value(1)

def turn_led():
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)
    led.value(1)
    

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status()<0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting connection')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('Network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])
    return wlan

def send_uuid(url, uuid):

    wlan = connect_wifi()

    headers = {}
    payload = str(uuid)
    
    retry = True
    
    while retry:        
        try:
            print("sending...")
            response = requests.post(url, headers=headers, data=payload)
            print("sent (" + str(response.status_code) + "), status = " + str(wlan.status()) )
            response.close()
            turn_led()
            retry = False
            time.sleep(5)
        except Exception as e:
            print(e, "\n")
            print("could not connect (status=" + str(wlan.status()) + ")")
            
            if wlan.status() < 0 or wlan.status()>=3:
                print("trying to reconnect...")
                wlan.disconnect()
                wlan.connect(ssid, password)
                if wlan.status() == 3:
                    print('connected')
                else:
                    print('failed')
                    retry = False
            time.sleep(1)
