#https://www.tomshardware.com/how-to/send-and-receive-data-raspberry-pi-pico-w-mqtt
import network
import machine
import utime
from machine import Pin
from umqtt.simple import MQTTClient
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
ssid = 'lasmussen'
password = '19660729'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

utime.sleep(5)
print(wlan.isconnected())

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_onboard.value(0)

WIDTH =128

HEIGHT= 64

i2c=I2C(0,scl=Pin(5),sda=Pin(4),freq=200000)

oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

write15 = Write(oled, ubuntu_mono_15)

write20 = Write(oled, ubuntu_mono_20)


mqtt_server = '192.168.1.60'
client_id = 'mqtt'
topic_sub = b'WLED/dht/temperature'
topic_sub2 = b'WLED/dht/humidity'


def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    floating_number = float(msg)
    if floating_number>40:
        write20.text(msg + " humidity" , 0, 20)
    else:
        write20.text(msg + "*C" , 0, 0)
    oled.show()


def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    utime.sleep(5)
    machine.reset()
    
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    client.subscribe(topic_sub)
    client.subscribe(topic_sub2)
    utime.sleep(1)