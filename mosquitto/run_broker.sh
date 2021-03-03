#!/bin/bash

sudo sed "s|CA_CERT_DIR|$PWD|g" mosquitto.conf > use_this.conf

sudo mosquitto -v -c ./use_this.conf

