# ESP32 MQTT Simulator

A Python program to simulate ESP32 connecting to MQTT broker and sending random data every 2 seconds.

## Installation

1. Install required libraries:
```bash
pip install -r requirements.txt
```

2. Setup configuration file:
```bash
# Copy .env.example to .env
cp .env.example .env
```

3. Edit `.env` file and fill with your MQTT configuration:
```
MQTT_BROKER=your_broker_address
MQTT_PORT=1883
MQTT_TOPIC=your_topic_here
```

## How to Run

```bash
python esp32_mqtt_simulator.py
```

## Configuration

All configurations are stored in `.env` file (will not be pushed to GitHub):
- `MQTT_BROKER`: MQTT broker address
- `MQTT_PORT`: MQTT broker port
- `MQTT_TOPIC`: Topic for publishing data

## Features

- Sends celsius data (0-100°C) every 2 seconds
- Displays data in terminal
- Secure configuration with .env file

## Stop Program

Press `Ctrl+C` to stop the program.
