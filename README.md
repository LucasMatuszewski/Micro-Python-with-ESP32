# MicroPython Weather Station with ESP32

My IOT Weather Station build with:

- ESP32 micro controller (NodeMCU-32S dev-kit, 2-core),
- OLED SSD1306 display,
- BME280 sensor (temperature, humidity, pressure).

## Main features:

- 2 separate threads with `_thread` to use 2-cores:
  - 1st for data collecting and displaying on OLED screen (every 5 seconds),
  - 2nd for ~~Web Server with sockets~~ sending to API (every 15 minutes).
    - Web Server commented to save memory and fix the Error 16 (device or resource busy)
    - sending to API blocked main code (sensors & oled) for a while so moved to 2nd thread
    - Build in blue LED turns on while sending to API
    - Sends to API average sensor values for last 15 minutes (but maybe sending last values will be better for performance and memory?)
- Build-in button turns off displaying data on the OLED (to don't burn-in the screen)
  - we don't power off the OLED to still display errors (but maybe should change it for energy efficiency when running on battery?)
- Error counters to soft restart a device (on 5th error) or exit while loop on 10th
  - on any error or infinite loop I couldn't send files to fix the bug and have to erase an old flash and flash with MicroPython again (maybe there is a better way?)
- **REST API** to save data from ESP32 in database:
  - **Firestore** DB because it's in GCN's _free tier_ and I wanted to learn it
  - SQL querying will be more suitable for this so maybe I will refactor it in the future
  - basic POST security with secret in ENV variable
  - basic endpoints to get data by place (office, home, etc.) and with limit
- Served from **Docker** container with Google **Cloud Run**
- Continuos Deployment with GitHub repo mirroring to **Cloud Source** and Google **Cloud Build**

## My plans:

- More endpoints to filter data, make statistics (by hour of day, day of week, periods), prepare them for charts and analysis.
- React App to display data with filters and charts to analyze trends (by day of week, by hour of day etc).
- Web sockets to update chart live? PWA for offline capabilities?
