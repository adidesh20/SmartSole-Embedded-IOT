import smbus2
import time

class ThermopileSensor():
    def __init__(self, bus, address=0x40, sampling_rate=0x800):
        """ Initializes a thermopile sensor for communication.

        Args:
            bus  (smbus2.SMBus)  : bus that will be used to communicate
            address       (int)  : address of the thermopile device on the bus
            sampling_rate (int)  : {0x0, 0x200, 0x400, 0x600, 0x800} sampling rate for thermopile sensor
        
        Raises:
            RuntimeError: faulty wiring, was unable to communicate with device
        """
        self.bus = bus
        self.ADDR = address

        assert sampling_rate in (0x0, 0x200, 0x400, 0x600, 0x800)

        self._REG = {
            "CONFIG"      : 0x02,
            "WHO_AM_I"    : 0xFF,
        }

        
        # create some simple lambdas to shorthand reading and writing messages
        read = lambda x: smbus2.i2c_msg.read(self.ADDR, x)
        write = lambda x: smbus2.i2c_msg.write(self.ADDR, x)
        
        # activate the sensor
        bus.i2c_rdwr( write( [ self._REG['CONFIG'], (0x71 | sampling_rate >> 8), sampling_rate & 0xFF ] ) )

        # testing if properly connected
        device_id_reader = read(2) 
        self.bus.i2c_rdwr( write( [ self._REG['WHO_AM_I'] ] ) , device_id_reader )

        # try most basic communication, this is a read-only register set to the device id
        print('device id: {}'.format(int.from_bytes(device_id_reader.buf[0]+device_id_reader.buf[1], 'big')))
        if int.from_bytes(device_id_reader.buf[0]+device_id_reader.buf[1], 'big') != 0x67:
            raise RuntimeError("Thermopile sensor not found, check your wiring")

        self._read = read
        self._write = write
        self._temp_request = write( [0x1] )
        self._temp_reader = read( 2 )
        
    
    def activate(self):
        reader = self._read(2)
        self.bus.i2c_rdwr( self._write( [ self._REG['CONFIG'] ]), reader)
        res = int.from_bytes( reader.buf[0] + reader.buf[1], 'big' )
        self.bus.i2c_rdwr( self._write( [self._REG['CONFIG'] , (res >> 8) | 0x70, res & 0xFF] ) )

    def deactivate(self):
        reader = self._read(2)
        self.bus.i2c_rdwr( self._write( [self._REG['CONFIG']] ), reader)
        res = int.from_bytes( reader.buf[0] + reader.buf[1], 'big' )
        self.bus.i2c_rdwr( self._write( [self._REG['CONFIG'], (res>>8) & ~0x70, res & 0xFF] ) )

    def read(self):
        """Gets a reading from the thermopile

        Returns:
            temperature in celsius
        """

        read_ready = self._read(2)
        write_read_ready = self._write([self._REG['CONFIG']])
        ready = False
        while not ready:
            self.bus.i2c_rdwr( write_read_ready, read_ready )
            if (int.from_bytes(read_ready.buf[0] + read_ready.buf[1], 'big') & 0x80) != 0:
                ready = True

        self.bus.i2c_rdwr( self._temp_request, self._temp_reader )
        return (int.from_bytes( self._temp_reader.buf[0]+self._temp_reader.buf[1], 'big', signed="True" ) >> 2) / 32.0
    
    @property
    def get_reader(self):
        return self._gyro_reader


if __name__ == "__main__":
    bus = smbus2.SMBus(1)
    device = ThermopileSensor(bus)
    while True:
        print(device.read())
        time.sleep(0.1)