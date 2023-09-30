#https://www.tomshardware.com/how-to/send-and-receive-data-raspberry-pi-pico-w-mqtt
import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
ssid = 'lasmussen'
password = '19660729'


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

time.sleep(5)
print(wlan.isconnected())

Pin(20, Pin.OUT).on()
LED = Pin(14, Pin.OUT)

mqtt_server = '192.168.1.60'
client_id = 'mqtt'
topic_sub = b'rashberry_pico'


def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "on":
        LED.on()
    elif msg == "off":
        LED.off()

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()
    
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    client.subscribe(topic_sub)
    time.sleep(1)