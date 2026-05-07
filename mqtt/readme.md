# MQTT Broker Setup

This project uses a custom `mosquitto.conf` file for the local MQTT broker setup.

## Setup

1. Install Mosquitto locally.
2. Copy the `mosquitto.conf` file from this repo into the same folder as your local `mosquitto.exe`.
3. Open a terminal in that folder.
4. Run Mosquitto as a background process:

```powershell
.\mosquitto.exe -c .\mosquitto.conf -v
```

## Stopping the Broker

If Mosquitto is running as a background process, stop it from PowerShell with:

```powershell
Stop-Process -Name mosquitto
```

To check whether it is running first:

```powershell
Get-Process -Name mosquitto
```

If multiple Mosquitto processes are running, this will stop all of them:

```powershell
Stop-Process -Name mosquitto -Force
```