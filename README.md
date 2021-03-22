# MicroPython with ESP32
My IOT projects with ESP32 micro controller (NodeMCU-32S dev-kit, 2-core), OLED SSD1306 display, BME280 sensor (temperature, humidity, pressure).
2 separate threads with `_thread` (first for Web Server with sockets, second for data colacting and displaing on OLED).

## My plans:
- API to save data from ESP32 in SQL data base
- React App to display data live with web sockets and charts to analyse trends (by day, by hour etc).
