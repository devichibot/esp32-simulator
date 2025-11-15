import paho.mqtt.client as mqtt
import time
import random
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import pytz
from tzlocal import get_localzone

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
    
    # Get local timezone
    local_tz = get_localzone()
    print(f"Timezone: {local_tz}")
    print("-" * 50)
    
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
        lamp_state = True  # Start with lamp ON
        
        while True:
            counter += 1
            
            # Get current time in local timezone
            current_time = datetime.now(local_tz)
            
            # Randomly toggle lamp state every 10 iterations
            if counter % 10 == 0:
                lamp_state = not lamp_state
            
            # Generate random electrical data
            voltage = round(random.uniform(0, 220), 2)  # Voltage 0-220V
            current_amp = round(random.uniform(0, 10), 2)  # Current 0-10A
            power_watt = round(voltage * current_amp / 1000, 2)  # Power in kW
            
            # Create JSON payload
            payload = json.dumps({
                "power": "on" if lamp_state else "off",
                "voltage": voltage,
                "current": current_amp,
                "watt": power_watt
            })
            
            # Display in terminal with local time
            status = "ON" if lamp_state else "OFF"
            print(f"[{current_time.strftime('%H:%M:%S')}] Lamp: {status} | Voltage: {voltage}V | Current: {current_amp}A | Power: {power_watt}kW")
            
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
