import smbus2
import time

addr=0x40
bus = smbus2.SMBus(1)
write = smbus2.i2c_msg.write(addr, [0x01])
read = smbus2.i2c_msg.read(addr, 2)

write = smbus2.i2c_msg.write(addr, [0x01])
read = smbus2.i2c_msg.read(addr, 2)

i=0
while(True):
    time.sleep(0.1)
    bus.i2c_rdwr(read)
    print((int.from_bytes((read.buf[i+0]+read.buf[i+1]),'big', signed=True)>>2)//
32)

