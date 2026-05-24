"""
BindThings DHT22 Example
─────────────────────────
Reads temperature and humidity from DHT22 sensor
on Raspberry Pi and sends to BindThings every 15 seconds.

Wiring:
    DHT22 DATA → GPIO4 (Pin 7)
    DHT22 VCC  → 3.3V (Pin 1)
    DHT22 GND  → GND  (Pin 6)

Install:
    pip install bindthings Adafruit_DHT
"""

import time
import Adafruit_DHT
from bindthings import BindThings

TOKEN    = "YOUR_DEVICE_TOKEN"
DHT_PIN  = 4
DHT_TYPE = Adafruit_DHT.DHT22

bt = BindThings(TOKEN)
bt.connect()

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)

        if humidity is not None and temperature is not None:
            bt.send({
                "temperature": round(temperature, 1),
                "humidity":    round(humidity, 1),
            })
        else:
            print("[DHT22] Read error")

        time.sleep(15)  # FREE plan: 15s interval

except KeyboardInterrupt:
    bt.disconnect()
