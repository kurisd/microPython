import machine
led = machine.Pin("LED", machine.Pin.OUT)
led.off()
for i in range(29):
  gp = machine.Pin(i, machine.Pin.OUT)
  gp.off()