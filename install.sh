#!/usr/bin/env bash

set -x

# Get the user info first
read -p " Enter GPIO pin number the sensor is connected to: " GPIO_PINS
read -p " Enter room name: " ROOMS

export GPIO_PINS
export ROOMS


fail () {
    echo "$1"
    exit $2
}

apt update
apt install -y libgpiod2 python3-pip
retVal=$?
if [ $retVal -ne 0 ]; then
    fail "Error installing python-pip" $retVal
fi

python3 -m pip install --upgrade pip setuptools wheel
retVal=$?
if [ $retVal -ne 0 ]; then
    fail "Error installing setuptools wheel" $retVal
fi

python3 -m pip install adafruit-blinka RPI.GPIO adafruit-circuitpython-dht prometheus-client
retVal=$?
if [ $retVal -ne 0 ]; then
    fail "Error installing Adafruit_DHT" $retVal
fi


cat dht_exporter.service | envsubst > /etc/systemd/system/dht_exporter.service
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error creating /etc/systemd/system/dht_exporter.service"
fi

mkdir -p /opt/dht_exporter
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error creating folder /opt/dht_exporter"
fi

cp -r dht_exporter.py /opt/dht_exporter/dht_exporter.py
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error copying to /opt/dht_exporter/dht_exporter.py"
fi

systemctl enable dht_exporter.service

retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Error enabling dht_exporter.service"
fi
