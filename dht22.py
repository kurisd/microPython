from machine import Pin, I2C
from time import sleep
import dht
from ssd1306 import SSD1306_I2C
 
 
machine.Pin(2, machine.Pin.OUT).on()
sensor = dht.DHT22(Pin(27)) 
i2c=I2C(0,sda=Pin(4), scl=Pin(5), freq=400000)    #initializing the I2C method
oled = SSD1306_I2C(128, 64, i2c)
 
while True:
    oled.fill(0)
    sensor.measure()
    temp = str(sensor.temperature())
    hum = str(sensor.humidity())
    oled.text("Temperature",0,0)
    oled.text(temp +" C",0,10)
    oled.text("Humidity",0,35)
    oled.text(hum + " %",0,45)
    oled.show()
    sleep(2)