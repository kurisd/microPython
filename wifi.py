import time
import utime
import network
import ubinascii
ssid = 'lasmussen'
password = '19660729'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
# Wait for connect or fail
max_wait = 12
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print(mac)
    print(wlan.config('channel'))
    print(wlan.config('essid'))
    print(wlan.config('txpower'))
    
#led part
led1 = machine.Pin(17, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
led3 = machine.Pin(18, machine.Pin.OUT)
led4 = machine.Pin(19, machine.Pin.OUT)
led5 = machine.Pin(20, machine.Pin.OUT)
led6 = machine.Pin(22, machine.Pin.OUT)

led6.on()
led3.on()


def led():
    for i in range(29):
        if i != 23 and i != 24:
            machine.Pin(i).value(1)
            utime.sleep(0.3)
            machine.Pin(i).value(0)
    for i in range(28,-1,-1):
        if i != 23 and i != 24:
            machine.Pin(i).value(1)
            utime.sleep(0.3)
            machine.Pin(i).value(0)
            
    
for x in range(6):
    print(x)
    led()