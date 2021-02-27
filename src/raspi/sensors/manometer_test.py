from manometer2 import *
bus = smbus2.SMBus(1)

sensor = PressureSensor (bus)

while True:
    print (sensor.read())
    time.sleep(0.1)
