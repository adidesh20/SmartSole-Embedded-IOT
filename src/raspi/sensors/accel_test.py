from accelerometer import *
bus = smbus2.SMBus(1)

sensor = AccelerometerSensor(bus)

while True:
    print(sensor.read())
    time.sleep(0.1)
    
