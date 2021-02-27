import smbus2
import time

class AccelerometerSensor():
    def __init__(self, bus, address=0x1F, _range = 2):
        """ Initializes a accelerometer sensor for communication.
        Notes:
            - Remember you cannot read LSB without reading MSB as well
            - If you want to use a different range you have to make a new object

        Args:
            bus (smbus2.SMBus)  : bus that will be used to communicate
            address      (int)  : address of the accelerometer device on the bus
            range        (int)  : {2, 4 or 8}. This indicates the range of readings. The selected values are in G's.
        
        Raises:
            RuntimeError: faulty wiring, was unable to communicate with device
        """
        self.bus = bus
        self.ADDR = address
        self.range = _range

        self._SCALING_VALUES = { 2: 0.0078125, 4: 0.015625, 8: 0.03125,}
        self._scaling_factor = self._SCALING_VALUES[self.range]

        self._RANGE_SETTINGS = { 2: 0x00, 4: 0x01, 8: 0x02 }

        self._REG = {
            "OUT_X_MSB"   : 0x01,
            "OUT_X_LSB"   : 0x02,
            "OUT_Y_MSB"   : 0x03,
            "OUT_Y_LSB"   : 0x04,
            "OUT_Z_MSB"   : 0x05,
            "OUT_Z_LSB"   : 0x06,
            "WHO_AM_I"    : 0x0D,
            "DATA_CFG"    : 0x0E,
            "CTRL_REG_1"  : 0x2A,
            "CTRL_REG_2"  : 0x2B,
            "CTRL_REG_3"  : 0x2C,
            "CTRL_REG_4"  : 0x2D,
            "CTRL_REG_5"  : 0x2E,
        }
        
        # create some simple lambdas to shorthand reading and writing messages
        read = lambda x: smbus2.i2c_msg.read(self.ADDR, x)
        write = lambda x: smbus2.i2c_msg.write(self.ADDR, x)
        
        # testing if properly connected
        device_id_reader = read(1) 
        self.bus.i2c_rdwr( write( [ self._REG['WHO_AM_I'] ] ), device_id_reader )

        # try most basic communication, this is a read-only register set to the device id
        print('device id: {}'.format(int.from_bytes(device_id_reader.buf[0], 'big')))
        if int.from_bytes(device_id_reader.buf[0], 'big') != 0xD7:
            raise RuntimeError("Accelerometer / magenetometer sensor not found, check your wiring")

        range_setting = self._RANGE_SETTINGS[ self.range ]
        
        # go into standby mode
        self.bus.i2c_rdwr( write([ self._REG['CTRL_REG_1'], 0x00 ]) )
        # activate the sensor
        self.bus.i2c_rdwr( write([ self._REG['DATA_CFG'], range_setting ] ) )
        # go into active mode
        self.bus.i2c_rdwr( write([ self._REG['CTRL_REG_1'], 0x15 ]) )

        # set up the reader for all future readings
        self._accel_request = write( [ self._REG['OUT_X_MSB'] ] )
        self._accel_reader = read( 6 )
        # allow time to activate (>60ms as per datasheet)
        time.sleep(0.1)
    
    def read(self):
        """Gets a reading from the accelerometer sensor for x, y, z

        Returns:
            (int, int, int): returns (x, y, z) taken from the accelerometer sensor as a signed number in degrees.
        """
        self.bus.i2c_rdwr( self._accel_request, self._accel_reader )
        x = int.from_bytes(self._accel_reader.buf[0]+self._accel_reader.buf[1], 'big', signed=True) * self._scaling_factor
        y = int.from_bytes(self._accel_reader.buf[2]+self._accel_reader.buf[3], 'big', signed=True) * self._scaling_factor
        z = int.from_bytes(self._accel_reader.buf[4]+self._accel_reader.buf[5], 'big', signed=True) * self._scaling_factor
        return (x, y, z) 
    
    @property
    def get_reader(self):
        return self._accel_reader


if __name__ == "__main__":
    bus = smbus2.SMBus(1)
    device = AccelerometerSensor(bus)
    while True:
        print(device.read())