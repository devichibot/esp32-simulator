import paho.mqtt.client as mqtt
import time
import random
import json
import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv
import pytz
from tzlocal import get_localzone

# Load environment variables
load_dotenv()

# Konfigurasi MQTT dari .env
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt.ichibot.id")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
DEFAULT_TOPIC = os.getenv("MQTT_TOPIC", "j1mmf/main")

# Callback when successfully connected to broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        mqtt_topic = userdata.get('topic', 'unknown')
        client_id = userdata.get('client_id', 'unknown')
        print(f"✓ Connected to MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        print(f"✓ Client ID: {client_id}")
        print(f"✓ Publishing to topic: {mqtt_topic}")
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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='ESP32 MQTT Simulator')
    parser.add_argument('-t', '--topic', type=str, help='MQTT topic to publish to')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode - ask for topic')
    args = parser.parse_args()
    
    print("=" * 50)
    print("ESP32 MQTT Simulator")
    print("=" * 50)
    
    # Determine MQTT topic
    if args.topic:
        mqtt_topic = args.topic
        print(f"📢 Using topic from argument: {mqtt_topic}")
    elif args.interactive:
        mqtt_topic = input(f"📢 Enter MQTT topic (default: {DEFAULT_TOPIC}): ").strip()
        if not mqtt_topic:
            mqtt_topic = DEFAULT_TOPIC
    else:
        mqtt_topic = DEFAULT_TOPIC
        print(f"📢 Using default topic: {mqtt_topic}")
    
    # Generate client ID
    client_id = f"esp32_simulator_{random.randint(1000, 9999)}"
    
    # Get local timezone
    local_tz = get_localzone()
    print(f"Timezone: {local_tz}")
    print("-" * 50)
    
    # Initialize MQTT Client with callback API version
    client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.user_data_set({'topic': mqtt_topic, 'client_id': client_id})
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
        
        print("\nSending runtime data every 1 second...")
        print("Press Ctrl+C to stop\n")
        
        counter = 0
        lamp_state = True  # Start with lamp ON
        brightness = 50  # Start at 50% brightness
        
        while True:
            counter += 1
            
            # Get current time in local timezone
            current_time = datetime.now(local_tz)
            
            # Randomly toggle lamp state every 20 iterations
            if counter % 20 == 0:
                lamp_state = not lamp_state
                if lamp_state:
                    print(f"[{current_time.strftime('%H:%M:%S')}] 💡 LAMP TURNED ON")
                else:
                    print(f"[{current_time.strftime('%H:%M:%S')}] 🌙 LAMP TURNED OFF")
            
            # Slowly vary brightness when lamp is ON (simulate runtime changes)
            if lamp_state and counter % 5 == 0:
                brightness += random.randint(-10, 10)
                brightness = max(30, min(100, brightness))  # Keep between 30-100%
            
            if lamp_state:
                # Calculate base voltage from brightness
                base_voltage = (brightness / 100) * 220  # 0-220V
                
                # Add slight random fluctuations (±2%) to simulate real electrical variations
                voltage_variation = (random.random() - 0.5) * 0.04
                
                voltage = round(base_voltage * (1 + voltage_variation), 2)
            else:
                # When OFF, voltage is 0
                voltage = 0.0
            
            # Send only the voltage value as plain text
            payload = str(voltage)
            
            # Display in terminal with local time
            if lamp_state:
                print(f"[{current_time.strftime('%H:%M:%S')}] ⚡ Brightness: {brightness}% | Voltage: {voltage}V")
            else:
                print(f"[{current_time.strftime('%H:%M:%S')}] 🔴 OFF | Voltage: 0.0V")
            
            # Publish to MQTT
            result = client.publish(mqtt_topic, payload)
            
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"  ✗ Failed to send data")
            
            # Wait 1 second for more frequent updates
            time.sleep(1)
            
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
