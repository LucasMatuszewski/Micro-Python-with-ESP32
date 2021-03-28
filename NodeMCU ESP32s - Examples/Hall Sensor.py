import esp32
from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)

while True:
    hall = esp32.hall_sensor()
    print(hall)
    if hall > 80 :
        led.value(1)
    else :
        led.value(0)
    sleep(0.5)