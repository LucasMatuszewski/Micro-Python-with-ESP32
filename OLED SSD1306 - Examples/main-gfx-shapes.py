# Complete project details at https://randomnerdtutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/

# from machine import Pin, I2C
from machine import Pin, SoftI2C
from time import sleep
import ssd1306
import gfx

# ESP32 I2C Pin assignment
# SoftI2C(scl, sda, *, freq=400000, timeout=255) - RECOMENDED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# OLED Initialization
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# initiate drowing library from our gfx.py file
# arguments: size of drowing area (don't have to be entire screen), drowing function
graphics = gfx.GFX(oled_width, oled_height, oled.pixel)

# line(x0, y0, x1, y1, color)
graphics.line(0, 0, 127, 20, 1)

# rectangle(x0, y0, width, height, color)
graphics.rect(10, 15, 50, 30, 1)
graphics.fill_rect(15, 20, 15, 12, 1)

# circle(x0, y0, radius, color) - x/y for center
graphics.circle(80, 32, 10, 1)
graphics.fill_circle(80, 32, 5, 1)

# triangle(x0, y0, x1, y1, x2, y2, color)
graphics.triangle(70,45,60,63,110,50,1)
graphics.fill_triangle(72,48,66,59,92,52,1)

oled.show()
