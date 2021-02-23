#!/bin/bash

sudo cp -r certs/ /etc/mosquitto/certs/
sudo cp -r ca_certificates/ /etc/mosquitto/ca_certificates/

sudo touch /etc/mosquitto/mosquitto.conf
sudo sed "s|CA_CERT_DIR|$PWD|g" mosquitto.conf > use_this.conf

sudo mosquitto -v -c ./use_this.conf

