import machine
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
import utime

sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)
conversion_factor = 3.3 / (65535)

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_onboard.value(0)


WIDTH =128

HEIGHT= 64

i2c=I2C(0,scl=Pin(5),sda=Pin(4),freq=200000)

oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

write15 = Write(oled, ubuntu_mono_15)

write20 = Write(oled, ubuntu_mono_20)

print("alma")

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 -(reading - 0.706)/0.001721
    
    print(str(temperature) + "\n")
    write20.text(str(temperature) + "*C" , 0, 0)
    oled.show()
    
    utime.sleep(2)