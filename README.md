# Simulasi ESP32 MQTT

Program Python untuk simulasi ESP32 yang terhubung ke MQTT broker dan mengirim data random setiap 2 detik.

## Instalasi

1. Install library yang dibutuhkan:
```bash
pip install -r requirements.txt
```

2. Setup file konfigurasi:
```bash
# Copy file .env.example menjadi .env
cp .env.example .env
```

3. Edit file `.env` dan isi dengan konfigurasi MQTT Anda:
```
MQTT_BROKER=mqtt.ichibot.id
MQTT_PORT=1883
MQTT_TOPIC=your_topic_here
```

## Cara Menjalankan

```bash
python esp32_mqtt_simulator.py
```

## Konfigurasi

Semua konfigurasi disimpan di file `.env` (tidak akan di-push ke GitHub):
- `MQTT_BROKER`: alamat broker MQTT
- `MQTT_PORT`: port broker MQTT
- `MQTT_TOPIC`: topic untuk publish data

## Fitur

- Mengirim data celsius (0-100°C) setiap 2 detik
- Menampilkan data di terminal
- Konfigurasi aman dengan .env file

## Stop Program

Tekan `Ctrl+C` untuk menghentikan program.

## Push ke GitHub

File `.env` sudah ditambahkan ke `.gitignore`, sehingga konfigurasi sensitif Anda tidak akan terpush ke GitHub. Yang akan di-push hanya `.env.example` sebagai template.
