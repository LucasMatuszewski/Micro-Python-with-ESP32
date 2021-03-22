def web_page_weather(temp_string, hum_string, pres_string):
    try:
        print('FROM WEB_PAGE:', temp_string)
        html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,"><style>body { text-align: center; font-family: "Trebuchet MS", Arial;}
        table { border-collapse: collapse; width:35%; margin-left:auto; margin-right:auto; }
        th { padding: 12px; background-color: #0043af; color: white; }
        tr { border: 1px solid #ddd; padding: 12px; }
        tr:hover { background-color: #bcbcbc; }
        td { border: none; padding: 12px; }
        .sensor { color:white; font-weight: bold; background-color: #bcbcbc; padding: 1px;
        </style></head><body><h1>ESP with BME280</h1>
        <table><tr><th>MEASUREMENT</th><th>VALUE</th></tr>
        <tr><td>Temp. Celsius</td><td><span class="sensor">""" + temp_string + """</span></td></tr>
        <tr><td>Pressure</td><td><span class="sensor">""" + hum_string + """</span></td></tr>
        <tr><td>Humidity</td><td><span class="sensor">""" + pres_string + """</span></td></tr></body></html>"""
        return html
    except OSError as e:
        print('Error: ', e)
        print(e)
        print('Webpage error')
    except:
        print('Some Webpage Error', bme2)