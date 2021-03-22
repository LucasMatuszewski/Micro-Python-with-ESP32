# Sources:
# https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
# https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/

import _thread # to use two infinite loops we need to use two threads of our CPU (ESP32 has 2)
from time import sleep
from web_pages import web_page_weather

# create a new socket object called s with the given address family, and socket type (STREAM TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80)) # bind the socket to an IP address ('' or 'localhost') and port (80, but normally use >3000)
s.listen(5) # enable to accept connections with maximum 5 queued connections.

def sensorsThread():
    global oled
    counter = 0
    temp_sum = 0
    hum_sum = 0
    pres_sum = 0

    while True:
        try:
    #         GET DATA FROM SENSOR AS A STRING
    #         We dont have to import BME280 here, it's already imported in boot.py which runs before main.py
            temp_string = bme.temperature
            hum_string = bme.humidity
            pres_string = bme.pressure

    #         SHOW ON OLED SCREEN - oled is activated in boot.py
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

    #         COUNTER AND SUMS TO CALCULATE AVERAGE
            counter += 1
            temp_sum += temp
            hum_sum += hum
            pres_sum += pres

    #         EVERY X times send avarage data to an API (TODO, print for now)
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
            print('---- Error: ', e)
            oled.fill(0)
            oled.text('Sensor Error', 0, 10, 1)
            oled.show()
        except:
            print('Some Sensor Error')
#             oled.fill(0)
#             oled.text('Some Error', 0, 10, 1)
#             oled.show()
            
        sleep(5) # whait for 5s and repeat a while loop

def serverThread():
    while True:
        try:
    #         Free memory if it is too low
            if gc.mem_free() < 102000:
                gc.collect()
          
    #         ACCEPT NETWORK CONNECTIONS AND SEND WEB PAGES:
            conn, addr = s.accept()
            conn.settimeout(3.0)
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            conn.settimeout(None)
            request = str(request)
            print('Content = %s' % request)
            response = web_page_weather()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
            
        except OSError as e:
            print('---- Error: ', e)
            conn.close()
            print('Connection closed')
            oled.fill(0)
            oled.text('Connection Error', 0, 10, 1)
            oled.show()
        except:
            print('Some Connection Error')
#             oled.fill(0)
#             oled.text('Some Error', 0, 10, 1)
#             oled.show()

_thread.start_new_thread(sensorsThread, ())
_thread.start_new_thread(serverThread, ())