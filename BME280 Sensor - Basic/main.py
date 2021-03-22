# With the ESP32 you can set almost any pin to have I2C capabilities.
# You just need to set that in your code.

from machine import Pin, SoftI2C
from time import sleep
import ssd1306
import BME280


i2c_oled = SoftI2C(scl=Pin(32), sda=Pin(33))
i2c_sensor = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)

counter = 0
temp_sum = 0
hum_sum = 0
pres_sum = 0

while True:
    try:
#         GET DATA FROM SENSOR AS STRING
        bme = BME280.BME280(i2c=i2c_sensor)
        temp_string = bme.temperature
        hum_string = bme.humidity
        pres_string = bme.pressure

#         SHOW ON OLED SCREEN
        oled.fill(0)
        if temp_string != '0.00C':
            oled.text('Temp: ' + temp_string, 0, 10, 1)
        else:
            oled.text('Temp: ---', 0, 10, 1)
        if hum_string != '0.00%':
            oled.text('Hum: ' + hum_string, 0, 25, 1)
        else:
            oled.text('Hum: ---', 0, 25, 1)
        if pres_string != '0.00hPa':
            oled.text('Pres: ' + pres_string, 0, 40, 1)
        else:
            oled.text('Pres: ---', 0, 40, 1)
        oled.show()
        
#         GET DATA FROM SENSOR AS FLOATS (SHOULD I SEND RAW INTEGERS TO A SERVER?)
        temp = bme.read_temperature()/100
        hum = bme.read_humidity()/1024
        pres = bme.read_pressure()/256/100

#       COUNTER AND SUMS TO CALCULATE AVERAGE
        counter += 1
        temp_sum += temp
        hum_sum += hum
        pres_sum += pres

        if counter == 10:
            temp_average = round(temp_sum/counter, 2)
            hum_average = round(hum_sum/counter, 2)
            pres_average = round(pres_sum/counter, 2)
            print('Temperature: ', temp_average)
            print('Humidity: ', hum_average)
            print('Pressure: ', pres_average)
            
            counter = 0
            temp_sum = 0
            hum_sum = 0
            pres_sum = 0
        
    except OSError as e:
        print('Error:')
        print(e)
        oled.fill(0)
        oled.text('Sensor Error', 0, 10, 1)
        oled.show()
    except:
        print('Some Error')
    
    sleep(5)