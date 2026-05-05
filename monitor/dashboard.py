import os
import json
import threading
from datetime import datetime

import paho.mqtt.client as mqtt
from flask import Flask, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT   = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC  = os.getenv("MQTT_TOPIC", "wifi/nodes/+/rssi")

app   = Flask(__name__, static_folder="static")
nodes = {}
lock  = threading.Lock()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"MQTT connection failed: {reason_code}")
    else:
        client.subscribe(MQTT_TOPIC)
        print(f"Connected to broker, subscribed to {MQTT_TOPIC}")


def on_message(client, userdata, msg):
    try:
        data    = json.loads(msg.payload.decode())
        node_id = data.get("node_id", msg.topic.split("/")[2])
        with lock:
            nodes[node_id] = {
                "rssi":      data.get("rssi"),
                "ip":        data.get("ip"),
                "millis":    data.get("millis"),
                "last_seen": datetime.now().isoformat(),
            }
    except Exception as e:
        print(f"Message parse error: {e}")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/nodes")
def api_nodes():
    with lock:
        return jsonify(nodes)


def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    threading.Thread(target=start_mqtt, daemon=True).start()
    print("Dashboard running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
