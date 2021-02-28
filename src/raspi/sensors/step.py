from accelerometer import *
bus = smbus2.SMBus(1)


sensor = AccelerometerSensor(bus)
step=0
flag=0
while True:
    (x,y,z)=sensor.read()

    mag=(x*x+y*y+z*z)
    mag=(mag/10000)
    if( mag>2 and flag==0):
        step +-1
        flag=1
        print (step)
    elif mag<1.9:
        flag=0

    time.sleep(0.2)

