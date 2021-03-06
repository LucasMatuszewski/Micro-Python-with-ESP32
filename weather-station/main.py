# Sources:
# https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
# https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/

import _thread # to use two infinite loops we need to use two threads of our CPU (ESP32 has 2)
import urequests # to send HTTP requests
import ujson # to convert Python dictionary to JSON format
from time import sleep
from web_pages import web_page_weather

# create a new socket object called s with the given address family, and socket type (STREAM TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80)) # bind the socket to an IP address ('' or 'localhost') and port (80, but normally use >3000)
s.listen(5) # enable to accept connections with maximum 5 queued connections.

######
# @TODO refactor to less imperative & more DRY style using functions, like here:
# https://blog.miguelgrinberg.com/post/micropython-and-the-internet-of-things-part-vi-working-with-a-screen
# Add better error handling, move pin numbers and configs to config.py file
# Turn off display on button press - display.poweroff()
######

def sensorsThread():
    global temp_string
    global hum_string
    global pres_string

    counter = 0
    temp_sum = 0
    hum_sum = 0
    pres_sum = 0

    # @TODO switch 'place' with button or from settings fetched from online API (if available)
    current_place = 'office'
    api_status = ''
    from secrets import weather_api_key, weather_api_url # create secrets.py file with secret variables (not in GIT Repo)

    while True:
        try:
    #         GET DATA FROM SENSOR AS A STRING
    #         We dont have to import BME280 here, it's already imported in boot.py which runs before main.py
            temp_string = bme.temperature
            hum_string = bme.humidity
            pres_string = bme.pressure

    #         SHOW ON OLED SCREEN - oled is activated in boot.py
            oled.fill(0)
            if temp_string != '0.00C': # @TODO switch variable without repeating oled.text 2 times
                oled.text('Temp: ' + temp_string, 0, 5, 1)
            else:
                oled.text('Temp: ---', 0, 5, 1)
            if hum_string != '0.00%':
                oled.text('Hum: ' + hum_string, 0, 20, 1)
            else:
                oled.text('Hum: ---', 0, 20, 1)
            if pres_string != '0.00hPa':
                oled.text('Pres: ' + pres_string, 0, 35, 1)
            else:
                oled.text('Pres: ---', 0, 35, 1)
            oled.text('Place: ' + current_place, 0, 50, 1)
            # @TODO display icon, tutorial: https://blog.miguelgrinberg.com/post/micropython-and-the-internet-of-things-part-vi-working-with-a-screen
            if api_status == 'OK':
                oled.text('OK', 110, 5, 1)
            elif api_status != '':
                oled.text('X', 110, 5, 1)
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
            if counter == 180: # counter * sleep = delay (e.g. 120 * 5s = 600s = 10m
                temp_average = round(temp_sum/counter, 2)
                hum_average = round(hum_sum/counter, 2)
                pres_average = round(pres_sum/counter, 2)
                print('Temperature: ', temp_average)
                print('Humidity: ', hum_average)
                print('Pressure: ', pres_average)
                
                weather_data = {} # we use disctionary data structure
                weather_data["temperature"] = temp_average
                weather_data["humidity"] = hum_average
                weather_data["pressure"] = pres_average
                weather_data["placeId"] = current_place # @TODO switch place variable on button or settings from API
                weather_data["secretApiKey"] = weather_api_key # @TODO auth with token in header?
                weather_json = ujson.dumps(weather_data)
                # https://github.com/micropython/micropython-lib/blob/master/urequests/urequests.py#L103
                # post(url, data=None, json=None, headers={}, stream=None)
                response = urequests.post(weather_api_url, data = weather_json, headers = {'Content-Type': 'application/json'})
                api_status = response.text # show on OLED check icon for OK 200 and X for other responses
                response.close()
                
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
            response = web_page_weather(temp_string, hum_string, pres_string)
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