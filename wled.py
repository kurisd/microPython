import machine
import utime
import array, time
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio
import _thread

NUM_LEDS = 1
delay1 = 2

def bt3_transition():
    @asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,autopull=True, pull_thresh=24)
    def ws2812():
        T1 = 2
        T2 = 5
        T3 = 3
        label("bitloop")
        out(x, 1) .side(0) [T3 - 1]
        jmp(not_x, "do_zero") .side(1) [T1 - 1]
        jmp("bitloop") .side(1) [T2 - 1]
        label("do_zero")
        nop() .side(0) [T2 - 1]
        
    # Create the StateMachine with the ws2812 program, outputting on Pin(28).
    sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(28))

    # Start the StateMachine, it will wait for data on its FIFO.
    sm.active(1)

    # Display a pattern on the LEDs via an array of LED RGB values.
    ar = array.array("I", [0 for _ in range(NUM_LEDS)])


    # RGB demo
    def rgb_transition():
        # grb = 0, 0, inc
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j
            sm.put(ar,8)
            time.sleep_ms(delay1)
        
        # grb = 0, inc, 255
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j<<8 | 255
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = 0, 255, dec
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = 255<<8 | (255-j)
            sm.put(ar,8)
            time.sleep_ms(delay1)
            
        # grb = inc, 255, 0
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j<<16 | 255<<8 | 0
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = 255, dec, 0
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = 255<<16 | (255-j)<<8 | 0
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = 255, 0, inc
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = 255<<16 | j
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = 255, inc, 255
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = 255<<16 | j<<8 | 255
            sm.put(ar,8)
            time.sleep_ms(delay1)

        # grb = dec, dec, dec
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = (255-j)<<16 | (255-j)<<8 | (255-j)
            sm.put(ar,8)
            time.sleep_ms(delay1)
        
    rgb_transition()
    
for x in range(6):
    print(x)
    bt3_transition()