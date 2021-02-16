from gyroscope import *

bus = smbus2.SMBus(1)

gyro = GyroscopeSensor(bus)
