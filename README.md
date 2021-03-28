# MicroPython Weather Station with ESP32

My IOT Weather Station build with:

- ESP32 micro controller (NodeMCU-32S dev-kit, 2-core),
- OLED SSD1306 display,
- BME280 sensor (temperature, humidity, pressure).

## Main features:

- 2 separate threads with `_thread` to use 2-cores:
  - 1st for data collecting, sending to API (every 15 minutes) and displaying on OLED screen (every 5 seconds),
  - 2nd for Web Server with sockets.
- **REST API** to save data from ESP32 in data base:
  - **Firestore** DB because it's in GCN's _free tier_ and I wanted to learn it
  - SQL querying will be more suitable for this so maybe I will refactor it in future
  - basic POST security with secret in ENV variable
  - basic endpoints to get data by place (office, home, etc.) and with limit
- Served from **Docker** container with Google **Cloud Run**
- Continuos Deployment with GitHub repo mirroring to **Cloud Source** and Google **Cloud Build**

## My plans:

- More endpoints to filter data, make statistics (by hour of day, day of week, periods), prepare them for charts and analysis.
- React App to display data with filters and charts to analyse trends (by day of week, by hour of day etc).
- Web sockets to update chart live? PWA for offline capabilities?
