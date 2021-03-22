# Complete project details at https://randomnerdtutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/

# from machine import Pin, I2C
from machine import Pin, SoftI2C
import ssd1306
from time import sleep

# ESP32 I2C Pin assignment
# SoftI2C(scl, sda, *, freq=400000, timeout=255) - RECOMENDED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# OLED Initialization
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Scroll in screen horizontally from left to right
def scroll_in_screen(screen):
  for i in range (0, oled_width+1, 4):
    for line in screen:
      oled.text(line[2], -oled_width+i, line[1])
    oled.show()
    if i!= oled_width:
      oled.fill(0)

# Scroll out screen horizontally from left to right    
def scroll_out_screen(speed):
  for i in range ((oled_width+1)/speed):
    for j in range (oled_height):
      oled.pixel(i, j, 0)
    oled.scroll(speed,0) # scrolls entire screen
    oled.show()
    
# Continuous horizontal scroll
def scroll_screen_in_out(screen):
  for i in range (0, (oled_width+1)*2, 1):
    for line in screen:
      oled.text(line[2], -oled_width+i, line[1])
    oled.show()
    if i!= oled_width:
      oled.fill(0)
 
# Scroll in screen vertically 
def scroll_in_screen_v(screen):
  for i in range (0, (oled_height+1), 1):
    for line in screen:
      oled.text(line[2], line[0], -oled_height+i+line[1])
    oled.show()
    if i!= oled_height:
      oled.fill(0)
      
# Scroll out screen vertically 
def scroll_out_screen_v(speed):
  for i in range ((oled_height+1)/speed):
    for j in range (oled_width):
      oled.pixel(j, i, 0)
    oled.scroll(0,speed)
    oled.show()

# Continous vertical scroll
def scroll_screen_in_out_v(screen):
  for i in range (0, (oled_height*2+1), 1):
    for line in screen:
      oled.text(line[2], line[0], -oled_height+i+line[1])
    oled.show()
    if i!= oled_height:
      oled.fill(0)


# lines to display in scroll
line1 = 'Hello Hania !'

# text() accepts only Strings. Sensors usually returns numbers. We have to convert
temperature = 21.54
temp_string = str(temperature)
line2 = 'Temp: ' + temp_string + ' C'

line3 = 'BM + LM + HM'

screen1 = [[0, 0, line1], [0, 16, line2], [0, 32, line3]]
screen2 = [[0, 0, line1], [0, 16, line3]]
screen3 = [[0, 40, line3]]

while True:
    # Scroll in, stop, scroll out (horizontal)
    scroll_in_screen(screen1)
    sleep(2)
    scroll_out_screen(4)

    # Continuous horizontal scroll
    scroll_screen_in_out(screen2)
    scroll_screen_in_out(screen3)

    # Scroll in, stop, scroll out (vertical)
    scroll_in_screen_v(screen1)
    sleep(2)
    scroll_out_screen_v(4)

    scroll_in_screen_v(screen2)
    sleep(2)
    scroll_out_screen_v(4)

    scroll_in_screen_v(screen3)
    sleep(2)
    scroll_out_screen_v(4)

    # Continuous verticall scroll 
    scroll_screen_in_out_v(screen1)
    scroll_screen_in_out_v(screen2)
    scroll_screen_in_out_v(screen3)
