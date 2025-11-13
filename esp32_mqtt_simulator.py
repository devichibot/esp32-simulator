import paho.mqtt.client as mqtt
import time
import random
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi MQTT dari .env
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt.ichibot.id")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "default/topic")
CLIENT_ID = f"esp32_simulator_{random.randint(1000, 9999)}"

# Callback when successfully connected to broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✓ Connected to MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        print(f"✓ Client ID: {CLIENT_ID}")
        print(f"✓ Publishing to topic: {MQTT_TOPIC}")
        print("-" * 50)
    else:
        print(f"✗ Connection failed, error code: {rc}")

# Callback when message is successfully published
def on_publish(client, userdata, mid, reason_code=None, properties=None):
    pass  # Silent publish

# Callback when disconnected from broker
def on_disconnect(client, userdata, rc, properties=None, reason_code=None):
    if rc != 0:
        print(f"\n✗ Disconnected from broker (code: {rc})")

def main():
    print("=" * 50)
    print("ESP32 MQTT Simulator")
    print("=" * 50)
    
    # Initialize MQTT Client with callback API version
    client = mqtt.Client(client_id=CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    try:
        # Connect to MQTT Broker
        print(f"Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Start loop in background
        client.loop_start()
        
        # Wait for connection
        time.sleep(2)
        
        print("\nSending random data every 2 seconds...")
        print("Press Ctrl+C to stop\n")
        
        counter = 0
        while True:
            counter += 1
            
            # Generate random celsius data
            celsius = round(random.uniform(0.0, 100.0), 2)
            
            # Send only numeric value
            payload = str(celsius)
            
            # Display in terminal
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Celsius: {celsius}°C")
            
            # Publish to MQTT
            result = client.publish(MQTT_TOPIC, payload)
            
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"  ✗ Failed to send data")
            
            # Wait 2 seconds
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n✓ Program stopped by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        print("Closing connection...")
        client.loop_stop()
        client.disconnect()
        print("✓ Connection closed")

if __name__ == "__main__":
    main()
