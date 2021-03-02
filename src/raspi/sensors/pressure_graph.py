import gpiozero
from manometer import *
import matplotlib.pyplot as plt

bus = smBus2.SMBus(1)
sensor = PressureSensor(bus)
button = Button(21)
readingsY = []
timesX = []

button.wait_for_press()

t_end = time.time() + 30
t0 = time.clock()
while time.time() < t_end:
    
    reading = sensor.read()
    elapsed = time.clock() - t0
    readingsY.append(reading)
    timesX.append(elapsed)

plt.plot(timesX,readingsY)
plt.xlabel('Time')
plt.ylabel('Presure')
plt.savefig('pressure_graph.png')



