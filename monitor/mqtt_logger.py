import csv
import json
import os
from datetime import datetime

import paho.mqtt.client as mqtt

# =========================
# USER SETTINGS
# =========================
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "wifi/nodes/+/rssi"
CSV_FILE = "rssi_log.csv"

# =========================
# CSV SETUP
# =========================
def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp_utc",
                "topic",
                "node_id",
                "rssi",
                "ip",
                "millis",
                "raw_payload"
            ])

# =========================
# MQTT CALLBACKS
# =========================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect, return code: {rc}")

def on_message(client, userdata, msg):
    timestamp = datetime.utcnow().isoformat()

    try:
        payload_text = msg.payload.decode("utf-8")
        data = json.loads(payload_text)

        node_id = data.get("node_id", "")
        rssi = data.get("rssi", "")
        ip = data.get("ip", "")
        millis = data.get("millis", "")

        print(f"[{timestamp}] {msg.topic} | node={node_id} | rssi={rssi}")

        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                msg.topic,
                node_id,
                rssi,
                ip,
                millis,
                payload_text
            ])

    except Exception as e:
        print(f"Error processing message on topic {msg.topic}: {e}")
        print(f"Raw payload: {msg.payload!r}")

# =========================
# MAIN
# =========================
def main():
    ensure_csv_exists()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to broker at {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    client.loop_forever()

if __name__ == "__main__":
    main()