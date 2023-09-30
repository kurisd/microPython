import network
import socket
import time
import struct
#oled
import machine
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20, ubuntu_condensed_12, ubuntu_15
import utime
#temp
import dht 
from machine import Pin

sensor = dht.DHT22(Pin(27))

#time ntp
NTP_DELTA = 2208988800
host = "pool.ntp.org"

ssid = 'lasmussen'
password = '19660729'
hrs_offset = 1

def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA + hrs_offset * 3600   
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

set_time()

print(time.localtime())

sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)
conversion_factor = 3.3 / (65535)

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_onboard.value(0)


WIDTH =128

HEIGHT= 64

i2c=I2C(0,scl=Pin(5),sda=Pin(4),freq=200000)

oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

gfx = GFX(128, 64, oled.pixel)
write15 = Write(oled, ubuntu_mono_15)

write20 = Write(oled, ubuntu_mono_20)

write12 = Write(oled, ubuntu_condensed_12)

writeB =  Write(oled, ubuntu_15)

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 -(reading - 0.706)/0.001721
    
    #temp
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    #print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))
    
    writeB.text(str(temperature) + "*C" , 0, 0,bgcolor=1, color=0)
    write12.text(str(time.localtime()), 0, 15,bgcolor=0, color=1)
    gfx.line(0, 30, 127, 30, 1)
    gfx.line(0, 31, 127, 31, 1)
    write15.text(str("Temperature: {}C".format(temp-3)),0,35,bgcolor=0, color=1)
    write15.text(str("Humidity: {:.0f}%".format(hum)),0,50,bgcolor=0, color=1)
    oled.show()
    
    utime.sleep(1)