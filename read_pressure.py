import time
import smbus2

ADDR = 0x18
bus = smbus2.SMBus(1)
write = smbus2.i2c_msg.write(ADDR, [0xaa, 0x00, 0x00])

while (True):
  bus.i2c_rdwr(write)
  time.sleep(0.5)
  read = smbus2.i2c_msg.read(ADDR, 4)
  bus.i2c_rdwr(read)
  pressure = int.from_bytes(read.buf[1]+read.buf[2]+read.buf[3], 'big')
  print(pressure)
