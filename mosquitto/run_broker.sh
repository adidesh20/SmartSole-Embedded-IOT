#!/bin/bash

sudo cp -r certs/ /etc/mosquitto/certs/
sudo cp -r ca_certificates/ /etc/mosquitto/ca_certificates/

sudo touch /etc/mosquitto/mosquitto.conf
sudo sed "s|CA_CERT_DIR|$PWD|g" mosquitto.conf > tmp.conf

sudo cp tmp.conf /etc/mosquitto/
sudo mv /etc/mosquitto/tmp.conf /etc/mosquitto/mosquitto.conf

sudo mosquitto -v -c /etc/mosquitto/mosquitto.conf

