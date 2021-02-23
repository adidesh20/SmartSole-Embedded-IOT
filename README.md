# Embedded_IOT

## MQTT Setup
Under `/mosquitto/certificate_generation` run `generate.sh`. This will create the necessary certificates for TLS. Remember that when generating the server certificate you must use its domain as "Common Name" or TLS will not work. Also remember that the different certificates will need different details (location, name, organization) in order to not conflict with each other.

## MQTT Run
Under `/mosquitto` run `run_broker.sh`
