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

sensor = Pin(16, Pin.IN)

mqtt_server = '192.168.1.60'
client_id = 'mqtt'
topic_pub = b'rashberry_pico'
topic_msg = b'Movement Detected'

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    if sensor.value() == 0:
        client.publish(topic_pub, topic_msg)
        time.sleep(3)
    else:
        pass