#include <WiFi.h>
#include <PubSubClient.h>
#include "config.h"

// Publish interval in milliseconds
const unsigned long PUBLISH_INTERVAL = 5000;

// =========================
// GLOBALS
// =========================
WiFiClient espClient;
PubSubClient mqttClient(espClient);

unsigned long lastPublishTime = 0;

// =========================
// WIFI
// =========================
void connectToWiFi() {
  Serial.print("Connecting to Wi-Fi");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Wi-Fi connected");
  Serial.print("ESP32 IP address: ");
  Serial.println(WiFi.localIP());
}

// =========================
// MQTT
// =========================
void connectToMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT... ");

    // Client ID must be unique
    String clientId = String(NODE_ID) + "_client";

    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" retrying in 2 seconds");
      delay(2000);
    }
  }
}

// =========================
// RSSI PUBLISH
// =========================
void publishRSSI() {
  long rssi = WiFi.RSSI();

  String topic = String("wifi/nodes/") + NODE_ID + "/rssi";

  String payload = "{";
  payload += "\"node_id\":\"" + String(NODE_ID) + "\",";
  payload += "\"rssi\":" + String(rssi) + ",";
  payload += "\"ip\":\"" + WiFi.localIP().toString() + "\",";
  payload += "\"millis\":" + String(millis());
  payload += "}";

  bool ok = mqttClient.publish(topic.c_str(), payload.c_str());

  Serial.print("Published to ");
  Serial.println(topic);
  Serial.println(payload);

  if (!ok) {
    Serial.println("Publish failed");
  }
}

// =========================
// SETUP
// =========================
void setup() {
  Serial.begin(115200);
  delay(1000);

  connectToWiFi();

  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  connectToMQTT();
}

// =========================
// LOOP
// =========================
void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi disconnected, reconnecting...");
    connectToWiFi();
  }

  if (!mqttClient.connected()) {
    connectToMQTT();
  }

  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublishTime >= PUBLISH_INTERVAL) {
    lastPublishTime = now;
    publishRSSI();
  }
}