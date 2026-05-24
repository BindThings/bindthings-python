"""
BindThings Basic Example
─────────────────────────
Sends temperature and humidity every 15 seconds.

Install:
    pip install bindthings
"""

import time
import json
from bindthings import BindThings

TOKEN = "YOUR_DEVICE_TOKEN"

bt = BindThings(TOKEN)

def on_command(payload: str):
    print(f"Command received: {payload}")
    data = json.loads(payload)
    # Handle command
    # e.g. if data.get("relay") == 1: GPIO.output(PIN, GPIO.HIGH)

bt.on_command(on_command)
bt.connect()

try:
    while True:
        bt.send({"temperature": 25.5, "humidity": 60})
        time.sleep(15)  # FREE plan: 15s interval
except KeyboardInterrupt:
    bt.disconnect()
