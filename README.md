# Embedded_IOT

## MQTT Setup
Under `/mosquitto/certificate_generation` run `generate.sh`. This will create the necessary certificates for TLS. Remember that when generating the server certificate you must use its domain as "Common Name" or TLS will not work. Also remember that the different certificates will need different details (location, name, organization) in order to not conflict with each other.

## MQTT Run
Under `/mosquitto` run `run_broker.sh`.

## Run server
Navigate to `/src/server/interface` and run `python3 index.py [ IP address of the machine running the MQTT broker ]`.
Open the url displayed to you on the terminal.

## Marketing website setup
Under `/website/assets/img` decompress the file `videos.rar` and place them in the same directory.
You can now go to the `/website` directory and by opening `index.html` in a browser you will be able to view the website (Google Chrome is suggested).

## Run Raspberry Pi Client
Clone either the entire directory or only the `/src/raspi/` folder to your Raspberry Pi. 
Navigate to the `/src/raspi/` folder on your pi, and run `python3 main.py [ IP address of the machine running the MQTT broker ]`.

## Troubleshooting Raspberry Pi
In case the sensors are loaded into i2c addresses different than the default ones, you can change these individually by navigating to the `/src/raspi/sensors/` directory and accessing the files named `accelerometer.py`, `manometer.py` and `thermopile.py` and changing the default values in the class constructors for `address`.
