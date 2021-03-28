# Complete project details at https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/

# from machine import Pin, I2C
from machine import Pin, SoftI2C
import ssd1306
from time import sleep

# ESP32 Pin assignment
# I2C(id, *, scl pin, sda pin, freq=400000) - DEPRECATED
# i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

# SoftI2C(scl, sda, *, freq=400000, timeout=255) - RECOMENDED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(1) # fill whole screen (1=blue, 0=black)

# text function arguments:
# string, X position, Y position, color (0=black, 1=blue=default)
oled.text('Hello, World 1 !', 0, 5, 0)
oled.text('Hello, World 2 !', 0, 20, 0)
oled.text('Hello, World 3 !', 0, 35, 0)

oled.pixel(94, 55, 0) # 1 pixel(X,Y,color)

oled.invert(True) # inverts colors (True/False)

# text() accepts only Strings. Sensors usually returns numbers. We have to convert
temperature = 21.54
temp_string = str(temperature)
oled.text('Temp: ' + temp_string + ' C', 0, 55, 0)
        
oled.show()