#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import random
import time
# import board
import adafruit_dht
from prometheus_client import start_http_server, Gauge

# Create a metric to track time spent and requests made.
g_temperature = Gauge('dht_temperature', 'Temperature in degrees celsius', ['room'])
g_humidity = Gauge('dht_humidity', 'Relative Humidity in percent', ['room'])


def update_sensor_data(dht_device, room):
    """Get sensor data and set on prometheus client."""

    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, give up until next data refresh.
        # print(error.args[0])
        return

    # Valid values for AM2303 are -40 to +80C +/- 0.5
    if abs(temperature) < 100:
        g_temperature.labels(room).set('{0:0.1f}'.format(temperature))

    # Valid humidity values for AM2303 are 0 to 99.9% +/- 2%RH
    if humidity >= 0 and humidity < 100:
        g_humidity.labels(room).set('{0:0.1f}'.format(humidity))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--poll_time", type=int, default=5, help="Poll sensor data every X seconds.")
    parser.add_argument("-g", "--gpio", type=int, nargs='+',
                        help="Set GPIO pin id to listen for DHT sensor data.",
                        required=True)
    parser.add_argument("-r", "--room", type=str, nargs='+',
                        help="Set room name.",
                        required=True)
    cli_arguments = parser.parse_args()

    if cli_arguments.poll_time < 2:
        print("INFO: The chip caches records for 2 seconds, so no improvement will be noticed with a frequent poll.")

    if len(cli_arguments.gpio) != len(cli_arguments.room):
        print("The number of gpio pins set needs to be the same as number of rooms set" \
              "\n Number of gpio pins: {g}\n Number of rooms: {r}".format(g=len(cli_arguments.gpio), r=len(cli_arguments.room)))
        exit(1)

    # Create DHT interfaces
    dht_interfaces = []
    for id, gpio_pin in enumerate(cli_arguments.gpio):
        # Initialise the dht device.
        dhtDevice = adafruit_dht.DHT22(gpio_pin)
        # Create a tuple of device and room name.
        dht_interfaces.append((dhtDevice, cli_arguments.room[id]))

    # Start up the server to expose the metrics.
    start_http_server(8001)

    # Update temperature and humidity
    while True:
        for dht_device, room in dht_interfaces:
            update_sensor_data(dht_device, room)
        time.sleep(cli_arguments.poll_time)
