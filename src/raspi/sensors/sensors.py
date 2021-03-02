import smbus2
import time
from accelerometer import *
from gyroscope import *
from manometer import *
from thermopile import *

class SensorInterface():
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        self.accelerometer = AccelerometerSensor(self.bus)
        self.gyroscope = GyroscopeSensor(self.bus)
        self.manometer = PressureSensor(self.bus)
        self.thermopile = ThermopileSensor(self.bus, sampling_rate=0x400)
    
    def read_as_dict(self):
        return {
            'accelerometer': self.accelerometer.read(),
            'gyroscope': self.gyroscope.read(),
            'manometer': self.manometer.read(),
            'thermopile': self.thermopile.read()
        }

    def read(self):
        return ( 
            self.accelerometer.read(),
            self.gyroscope.read(),
            self.manometer.read(),
            self.thermopile.read()
        )
        
if __name__ == '__main__':
    devices = SensorInterface()
    while True:
        print(devices.read_as_dict())
        time.sleep(0.1)