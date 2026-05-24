import json
import ssl
import time
import threading
import paho.mqtt.client as mqtt

BROKER  = "mqtt.bindthings.io"
PORT    = 8883
VERSION = "1.0.0"


class BindThings:
    """
    Official Python client for BindThings IoT Platform.

    Usage:
        bt = BindThings("YOUR_DEVICE_TOKEN")
        bt.connect()
        bt.send({"temperature": 25.5})
    """

    def __init__(self, token: str, client_id: str = None):
        self._token    = token
        self._client_id = client_id or f"bt_py_{token[:8]}"

        self._topic_telemetry  = f"devices/{token}/telemetry"
        self._topic_status     = f"devices/{token}/status"
        self._topic_commands   = f"devices/{token}/commands"
        self._topic_attributes = f"devices/{token}/attributes"

        self._command_cb = None
        self._connected  = False

        self._client = mqtt.Client(client_id=self._client_id)
        self._client.username_pw_set(token, token)

        # TLS — accept self-signed certificates
        self._client.tls_set(cert_reqs=ssl.CERT_NONE)
        self._client.tls_insecure_set(True)

        # LWT
        lwt = json.dumps({"online": False, "reason": "lwt"})
        self._client.will_set(self._topic_status, lwt, qos=1, retain=True)

        # Callbacks
        self._client.on_connect    = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message    = self._on_message

    # ── Public API ────────────────────────────────────────────────────────────

    def connect(self, blocking: bool = False) -> bool:
        """
        Connect to BindThings MQTT broker.

        Args:
            blocking: If True, run loop in foreground. If False, run in background thread.
        """
        print(f"[BindThings] Connecting to {BROKER}:{PORT}...")
        try:
            self._client.connect(BROKER, PORT, keepalive=60)
        except Exception as e:
            print(f"[BindThings] Connection failed: {e}")
            return False

        if blocking:
            self._client.loop_forever()
        else:
            self._client.loop_start()
            # Wait for connection
            timeout = 10
            while not self._connected and timeout > 0:
                time.sleep(0.5)
                timeout -= 0.5

        return self._connected

    def disconnect(self):
        """Disconnect from broker."""
        self.set_online(False)
        self._client.disconnect()
        self._client.loop_stop()
        self._connected = False
        print("[BindThings] Disconnected")

    def send(self, data: dict) -> bool:
        """
        Send telemetry data.

        Args:
            data: Dictionary of key-value pairs. e.g. {"temperature": 25.5}

        Returns:
            True if published successfully.
        """
        if not self._connected:
            print("[BindThings] Not connected")
            return False

        payload = json.dumps(data)
        result  = self._client.publish(self._topic_telemetry, payload, qos=0)
        ok      = result.rc == mqtt.MQTT_ERR_SUCCESS

        if ok:
            print(f"[BindThings] Sent: {payload}")
        else:
            print(f"[BindThings] Send failed: rc={result.rc}")

        return ok

    def send_attributes(self, data: dict) -> bool:
        """Send device attributes (non-timeseries data)."""
        if not self._connected:
            return False
        payload = json.dumps(data)
        result  = self._client.publish(self._topic_attributes, payload, qos=1)
        return result.rc == mqtt.MQTT_ERR_SUCCESS

    def set_online(self, online: bool = True) -> bool:
        """Set device online/offline status."""
        payload = json.dumps({"online": online})
        result  = self._client.publish(self._topic_status, payload, qos=1, retain=True)
        return result.rc == mqtt.MQTT_ERR_SUCCESS

    def on_command(self, callback):
        """
        Register a callback for incoming commands.

        Args:
            callback: Function(payload: str) called when command arrives.

        Example:
            def handle_command(payload):
                data = json.loads(payload)
                print(data)

            bt.on_command(handle_command)
        """
        self._command_cb = callback

    def is_connected(self) -> bool:
        """Check if connected to broker."""
        return self._connected

    # ── Private callbacks ─────────────────────────────────────────────────────

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._connected = True
            client.subscribe(self._topic_commands, qos=1)
            self.set_online(True)
            print("[BindThings] Connected ✓")
        else:
            self._connected = False
            print(f"[BindThings] Connect failed, rc={rc}")

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False
        if rc != 0:
            print(f"[BindThings] Unexpected disconnect, rc={rc}")

    def _on_message(self, client, userdata, msg):
        if msg.topic == self._topic_commands and self._command_cb:
            payload = msg.payload.decode("utf-8")
            print(f"[BindThings] Command: {payload}")
            self._command_cb(payload)
