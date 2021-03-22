from machine import Pin
from time import sleep
led = Pin(2, Pin.OUT)
counter = 0
while True:
  # led.value(not led.value())
  led.value(1)
  sleep(0.1)
  led.value(0)
  counter += 1
  print(counter)
  sleep(0.9)