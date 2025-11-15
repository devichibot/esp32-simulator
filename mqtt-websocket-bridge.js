// MQTT WebSocket Bridge Server
// This server acts as a bridge between browser (WebSocket) and MQTT broker (TCP)

const mqtt = require('mqtt');
const WebSocket = require('ws');
require('dotenv').config();

const MQTT_BROKER = process.env.MQTT_BROKER || 'mqtt.ichibot.id';
const MQTT_PORT = parseInt(process.env.MQTT_PORT) || 1883;
const WS_PORT = parseInt(process.env.WS_PORT) || 8080;

// Create WebSocket server
const wss = new WebSocket.Server({ port: WS_PORT });

console.log('='.repeat(50));
console.log('MQTT WebSocket Bridge Server');
console.log('='.repeat(50));
console.log(`WebSocket Server listening on port ${WS_PORT}`);
console.log(`MQTT Broker: ${MQTT_BROKER}:${MQTT_PORT}`);
console.log('Waiting for connections...\n');

wss.on('connection', (ws) => {
    console.log('✓ New WebSocket client connected');
    
    let mqttClient = null;
    let subscribedTopics = new Set();

    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);
            
            // Handle connection request
            if (data.type === 'connect') {
                const clientId = `bridge_${Math.random().toString(16).substr(2, 8)}`;
                
                mqttClient = mqtt.connect(`mqtt://${MQTT_BROKER}:${MQTT_PORT}`, {
                    clientId: clientId,
                    clean: true,
                    reconnectPeriod: 5000,
                });

                mqttClient.on('connect', () => {
                    console.log(`  ✓ MQTT connected for WebSocket client`);
                    ws.send(JSON.stringify({
                        type: 'connected',
                        message: 'Connected to MQTT broker'
                    }));
                });

                mqttClient.on('message', (topic, payload) => {
                    ws.send(JSON.stringify({
                        type: 'message',
                        topic: topic,
                        payload: payload.toString()
                    }));
                });

                mqttClient.on('error', (error) => {
                    console.error('  ✗ MQTT Error:', error.message);
                    ws.send(JSON.stringify({
                        type: 'error',
                        message: error.message
                    }));
                });

                mqttClient.on('close', () => {
                    console.log('  ✗ MQTT disconnected');
                    ws.send(JSON.stringify({
                        type: 'disconnected',
                        message: 'Disconnected from MQTT broker'
                    }));
                });
            }
            
            // Handle subscribe request
            else if (data.type === 'subscribe' && mqttClient) {
                const topic = data.topic;
                mqttClient.subscribe(topic, (err) => {
                    if (err) {
                        console.error(`  ✗ Subscribe error: ${err.message}`);
                        ws.send(JSON.stringify({
                            type: 'error',
                            message: `Subscribe failed: ${err.message}`
                        }));
                    } else {
                        subscribedTopics.add(topic);
                        console.log(`  ✓ Subscribed to: ${topic}`);
                        ws.send(JSON.stringify({
                            type: 'subscribed',
                            topic: topic
                        }));
                    }
                });
            }
            
            // Handle publish request
            else if (data.type === 'publish' && mqttClient) {
                const { topic, payload } = data;
                mqttClient.publish(topic, payload, (err) => {
                    if (err) {
                        console.error(`  ✗ Publish error: ${err.message}`);
                    } else {
                        console.log(`  ✓ Published to ${topic}`);
                    }
                });
            }
            
            // Handle disconnect request
            else if (data.type === 'disconnect' && mqttClient) {
                mqttClient.end();
                mqttClient = null;
            }
            
        } catch (error) {
            console.error('  ✗ Message parse error:', error.message);
        }
    });

    ws.on('close', () => {
        console.log('✗ WebSocket client disconnected');
        if (mqttClient) {
            mqttClient.end();
        }
    });

    ws.on('error', (error) => {
        console.error('✗ WebSocket error:', error.message);
    });
});

wss.on('error', (error) => {
    console.error('✗ WebSocket Server error:', error.message);
});

console.log('\nPress Ctrl+C to stop the server\n');
