# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

# Import sockets for network communication (both localhost and internet)
try:
  import usocket as socket
except:
  import socket

import network # to connect with WiFi
from machine import Pin, SoftI2C
# Pin to use ESP32 pins (GPIO = General Purpose Input Output)
# SoftI2C to use I2C (Inter-Integrated Circuit) serial communication bus to connect with OLED and BME280 sensor

# Turn off vendor OS debugging messages
import esp
esp.osdebug(None)

# Run a garbage collector to reclaim memory occupied by objects that are no longer used by the program
# This is useful to save space in the flash memory.
import gc
gc.collect()


# With the ESP32 you can set almost any pin to have I2C capabilities.
# You just need to set that in your code.

# import sensor library and set Pins for I2C
import BME280
i2c_sensor = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
bme = BME280.BME280(i2c=i2c_sensor)

# import OLED display library, set Pins for I2C and activate a screen
import ssd1306
i2c_oled = SoftI2C(scl=Pin(32), sda=Pin(33))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)


# set the ESP32 as a Wi-Fi station, activate it and make a connection with a router
from secrets import ssid, password
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# to ensure that code would not proceed while the ESP32 is not connected to our network
while station.isconnected() == False:
  pass

print('WiFi connection successful')
print(station.ifconfig()) # print network interface parameters (lik ESP32 IP address)

# we should address pins in Boot file also
# sensor = dht.DHT22(Pin(14))
# sensor = dht.DHT11(Pin(14))
led_blue = Pin(2, Pin.OUT) # Create a Pin object that refers to the ESP32 GPIO 2 === build in blue LED 