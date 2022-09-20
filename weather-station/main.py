# Sources:
# https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
# https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/

import _thread # to use two infinite loops we need to use two threads of our CPU (ESP32 has 2)
import sys
import urequests # to send HTTP requests
import ujson # to convert Python dictionary to JSON format
from time import sleep
# from web_pages import web_page_weather

######
# @TODO refactor to less imperative & more DRY style using functions, like here:
# https://blog.miguelgrinberg.com/post/micropython-and-the-internet-of-things-part-vi-working-with-a-screen
# Add better error handling, move pin numbers and configs to config.py file
# Turn off display after specified time (10 minutes?) - with time.ticks_ms/ticks_diff or machine.Timer() ?
######

def sensorsThread():
    global temp_string
    global hum_string
    global pres_string

    global counter
    global temp_sum
    global hum_sum
    global pres_sum    
    global api_status
    global oled_on
    global current_place

    counter = 0
    temp_sum = 0
    hum_sum = 0
    pres_sum = 0
    api_status = ''
    oled_on = True

    # @TODO switch 'place' with button or from settings fetched from online API (if available)
    current_place = 'PT office'

    thread1_err_count = 0

    while thread1_err_count < 10:
        try:                
            # GET DATA FROM SENSOR AS A STRING
            # We dont have to import BME280 here, it's already imported in boot.py which runs before main.py
            temp_string = bme.temperature
            hum_string = bme.humidity
            pres_string = bme.pressure

            # SHOW ON OLED SCREEN - oled is activated in boot.py
            oled.fill(0) # to clear the oled screen before displaying text (fill it all in black == off)
            if oled_on:
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
            oled.show() # always use fill(0) and show() (to clear error message when oled_on is False)

            # GET DATA FROM SENSOR AS FLOATS (SHOULD I SEND RAW INTEGERS TO A SERVER?)
            temp = bme.read_temperature()/100
            hum = bme.read_humidity()/1024
            pres = bme.read_pressure()/256/100

            # COUNTER AND SUMS TO CALCULATE AVERAGE
            counter += 1
            temp_sum += temp
            hum_sum += hum
            pres_sum += pres

        except OSError as e:
            print('---- Sensor or OLED Error: ', e)
            oled.fill(0)
            oled.text('Sensor Error', 0, 10, 1)
            oled.show()
            counter = 0
            temp_sum = 0
            hum_sum = 0
            pres_sum = 0
            thread1_err_count += 1
            if thread1_err_count >= 5: sys.exit('Reset on 5th Thread1 Error')
        except:
            print('Some Sensor/OLED Error')
            counter = 0
            temp_sum = 0
            hum_sum = 0
            pres_sum = 0
            thread1_err_count += 1
            # oled.fill(0)
            # oled.text('Some Error', 0, 10, 1)
            # oled.show()
            
        sleep(5) # wait for 5s and repeat a while loop


def serverThread():
    from secrets import weather_api_key, weather_api_url # create secrets.py file with secret variables (not in GIT Repo)

    # To change the value of a global variable inside a function, refer to the variable by using the global keyword:
    global counter
    global temp_sum
    global hum_sum
    global pres_sum    
    global api_status
    global oled_on
    api_err_count = 0
    thread2_err_count = 0

    # create a new socket object called s with the given address family, and socket type (STREAM TCP)
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('', 80)) # bind the socket to an IP address ('' or 'localhost') and port (80, but normally use >3000)
    # s.listen(5) # enable to accept connections with maximum 5 queued connections.
    
    while thread2_err_count < 10:
        try:
            # Free memory if it is too low
            if gc.mem_free() < 20000:
                # print('mem_free: ', gc.mem_free())
                # print('mem_alloc: ', gc.mem_alloc()) # free+alloc = 111168 bytes (111 KB of heap RAM? ESP32 should have 320 KB RAM in total)
                gc.collect()
            
            # EVERY X times send average data to an API
            if counter == 180: # counter * sleep = delay (e.g. 120 * 5s = 600s = 10m
                temp_average = round(temp_sum/counter, 2)
                hum_average = round(hum_sum/counter, 2)
                pres_average = round(pres_sum/counter, 2)
                # print('Temperature: ', temp_average)
                # print('Humidity: ', hum_average)
                # print('Pressure: ', pres_average)
                
                weather_data = {} # we use dictionary data structure
                weather_data["temperature"] = temp_average
                weather_data["humidity"] = hum_average
                weather_data["pressure"] = pres_average
                weather_data["placeId"] = current_place # @TODO switch place variable on button or settings from API
                weather_data["secretApiKey"] = weather_api_key # @TODO auth with token in header?
                weather_json = ujson.dumps(weather_data)
                try:
                    led_blue.value(1) # turn on build in Blue LED while sending to API
                    # https://github.com/micropython/micropython-lib/blob/master/urequests/urequests.py#L103
                    # post(url, data=None, json=None, headers={}, stream=None)
                    response = urequests.post(weather_api_url, data = weather_json, headers = {'Content-Type': 'application/json'})
                    api_status = response.text # show on OLED "OK" for OK 200 and X for other responses
                    # print('Response: ', response.__dict__)
                    # __dict__ prints: {'encoding': 'utf-8', 'raw': <_SSLSocket 3ffec310>, 'reason': b'OK', '_cached': None, 'status_code': 200}
                    if response.text or response.status_code: # turn off Blue LED when we have any response
                        led_blue.value(0)
                    if api_status == 'OK': api_err_count = 0 # Restart error counter on response 200 OK
                    response.close()
                except OSError as e:
                    print('---- API Error: ', e) # 16 == "device or resource busy"
                    oled.fill(0)
                    oled.text('API Error', 0, 10, 1)
                    oled.show()
                    led_blue.value(0)
                    api_status = 'Error'
                    counter = 0
                    temp_sum = 0
                    hum_sum = 0
                    pres_sum = 0
                    api_err_count += 1 # increase errors by 1
                    if api_err_count >= 5: sys.exit('Reset on 5th API Error')
                
                counter = 0
                temp_sum = 0
                hum_sum = 0
                pres_sum = 0


            # TURN OFF/ON THE OLED on Boot button press
            # - in 2nd thread because 1st thread sleeps for 5 seconds and won't read a button on each click
            # - after sending to API to don't interrupt sending by pushing a button (it sleeps for 0.5s)
            # - sleep won't affect data sent to API because counter and _sum's are calculated at 1st thread
            if button_boot.value() == False: # value is False when button is pressed (strange, why?)
                led_blue.value(1)
                oled_on = not oled_on #toggle the oled_on value
                if oled_on == False:
                    oled.fill(0) # we just clear the screen (fill it in black) but still shows errors. But maybe we should power off/on the screen for energy savings?
                    oled.show()
                else:
                    oled.fill(0)
                    oled.text('Display ON :)', 0, 10, 1)
                    oled.text('Loading...', 0, 25, 1)
                    oled.show()
                sleep(0.5) # without sleep it's hard to push a button only once (have to be very fast)
            else:
                led_blue.value(0)

            # ACCEPT NETWORK CONNECTIONS AND SEND WEB PAGES:
            # conn, addr = s.accept()
            # conn.settimeout(3.0)
            # print('Got a connection from %s' % str(addr))
            # request = conn.recv(1024)
            # conn.settimeout(None)
            # request = str(request)
            # print('Content = %s' % request)
            # response = web_page_weather(temp_string, hum_string, pres_string)
            # conn.send('HTTP/1.1 200 OK\n')
            # conn.send('Content-Type: text/html\n')
            # conn.send('Connection: close\n\n')
            # conn.sendall(response)
            # conn.close()
            
        except OSError as e:
            print('---- 2nd Thread Error: ', e)
            # conn.close()
            # print('Connection closed')
            oled.fill(0)
            oled.text('2nd Thread Error', 0, 10, 1)
            thread2_err_count += 1
            oled.show()
            if thread2_err_count >= 5: sys.exit('Reset on 5th Thread2 Error')
        except:
            print('Some 2nd Thread Error')
            thread2_err_count += 1
            if thread2_err_count >= 5: sys.exit('Reset on 5th Thread2 Error')
            # oled.fill(0)
            # oled.text('Some Error', 0, 10, 1)
            # oled.show()

_thread.start_new_thread(sensorsThread, ())
_thread.start_new_thread(serverThread, ())
