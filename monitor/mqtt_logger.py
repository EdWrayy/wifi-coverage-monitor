import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "wifi/nodes/+/rssi"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to {MQTT_TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"{msg.topic}: {payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()