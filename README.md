# dht-exporter
Prometheus exporter for humidity and temperature sensor data (DHT22, DHT11, AM2302) running on Raspberry pi, with Rasbian.

## Wiring

Reference pinout for AM2302 and Raspberry Pi 2 Model B:

| Wire   | Header | Description |
| -----  | ------ | ----------- |
| Red    | pin 1  | +3.3v       |
| Black  | pin 6  | Ground      |
| Yellow | pin 4  | GPIO Data   |
