# MQTT Broker Setup

This project uses a custom `mosquitto.conf` file for the local MQTT broker setup.

## Setup

1. Install Mosquitto locally.
2. Copy the `mosquitto.conf` file from this repo into the same folder as your local `mosquitto.exe`.
3. Open a terminal in that folder.
4. Run (for Windows):

```powershell
.\mosquitto.exe -c .\mosquitto.conf -v