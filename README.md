# BindThings Python

Official Python client for the [BindThings](https://bindthings.com) IoT Platform.

## Installation

```bash
pip install bindthings
```

## Quick Start

```python
from bindthings import BindThings

bt = BindThings("YOUR_DEVICE_TOKEN")
bt.connect()
bt.send({"temperature": 25.5, "humidity": 60})
```

## API Reference

### Constructor
```python
bt = BindThings(token, client_id=None)
```

### Connect
```python
bt.connect()              # Background thread (non-blocking)
bt.connect(blocking=True) # Foreground (blocking)
```

### Send Telemetry
```python
bt.send({"temperature": 25.5})
bt.send({"temperature": 25.5, "humidity": 60, "pressure": 1013})
```

### Receive Commands
```python
def on_command(payload: str):
    import json
    data = json.loads(payload)
    print(data)

bt.on_command(on_command)
```

### Status
```python
bt.set_online(True)   # Mark device as online
bt.set_online(False)  # Mark device as offline
bt.is_connected()     # Check connection
bt.disconnect()       # Graceful disconnect
```

## Examples

| Example | Description |
|---------|-------------|
| [basic.py](examples/basic.py) | Send temperature and humidity every 15 seconds |
| [dht22.py](examples/dht22.py) | Read DHT22 on Raspberry Pi and send to BindThings |

## Connection Details

| Parameter | Value |
|-----------|-------|
| Broker | `mqtt.bindthings.io` |
| Port | `8883` (TLS) |
| Username | Your Device Token |
| Password | Your Device Token |

## License

MIT License — © 2025 BindThings
