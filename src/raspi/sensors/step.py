from sensors.accelerometer import *
bus = smbus2.SMBus(1)


class Step():
    def __init__(self):
        self.flag=0
    
    def is_step(self, reading):
        (x,y,z) = reading

        mag = (x*x+y*y+z*z)/10000
        if( mag >= 2 and self.flag == 0):
            self.flag=1
            return 1
        elif mag < 1.9:
            self.flag = 0
            return 0
        else:
            return 0
