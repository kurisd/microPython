import utime
import machine
import network

while True:
    led = machine.Pin("LED", machine.Pin.OUT)
    print("alma")
    utime.sleep(1)
    led.off()
    print("korte")
    utime.sleep(1)
    led.on()



