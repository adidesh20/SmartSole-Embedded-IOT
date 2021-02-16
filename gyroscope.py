import smbus2
import time

class GyroscopeSensor():
    def __init__(self, bus, address=0x21, sensitivity = 250):
        """ Initializes a gyroscope sensor for communication.
        Notes:
            - Remember you cannot read LSB without reading MSB as well
            - If you want to use a different sensitivity you have to make a new object

        Args:
            bus (smbus2.SMBus)  : bus that will be used to communicate
            address      (int)  : address of the gyroscope device on the bus
            sensitivity  (int)  : {250, 500, 1000 or 2000}. This indicates the sensitivity of the sensor
        
        Raises:
            RuntimeError: faulty wiring, was unable to communicate with device
        """
        self.bus = bus
        self.ADDR = address
        self.sensitivity = sensitivity

        self._SCALING_VALUES = { 250: 0.0078125, 500: 0.015625, 1000: 0.03125, 2000: 0.0625 }
        self._scaling_factor = self._SCALING_VALUES[self.sensitivity]

        self._SENSITIVITY_SETTINGS = { 250: 0x03, 500: 0x02, 1000: 0x01, 2000: 0x00, }

        self._REG = {
            "OUT_X_MSB"   : 0x01,
            "OUT_X_LSB"   : 0x02,
            "OUT_Y_MSB"   : 0x03,
            "OUT_Y_LSB"   : 0x04,
            "OUT_Z_MSB"   : 0x05,
            "OUT_Z_LSB"   : 0x06,
            "WHO_AM_I"    : 0x0C,
            "CTRL_REG_0"  : 0x0D,
            "CTRL_REG_1"  : 0x13,
            "CTRL_REG_2"  : 0x14,
            "CTRL_REG_3"  : 0x15,
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
            raise RuntimeError("FXAS21002C gyroscope sensor not found, check your wiring")

        sens_setting = self._SENSITIVITY_SETTINGS[ self.sensitivity ]
        
        # set the sensitivity of the gyroscope
        self.bus.i2c_rdwr( write([ self._REG['CTRL_REG_0'], sens_setting ]) )
        # activate the sensor
        self.bus.i2c_rdwr( write([ self._REG['CTRL_REG_1'], 0x0E ]) )

        # set up the reader for all future readings
        self._gyro_request = write( [ self._REG['OUT_X_MSB'] ] )
        self._gyro_reader = read( 6 )
        # allow time to activate (>60ms as per datasheet)
        time.sleep(0.1)
    
    def read(self):
        """Gets a reading from the gyroscope sensor for x, y, z

        Returns:
            (int, int, int): returns (x, y, z) taken from the gyroscope sensor as a signed number in degrees.
        """
        self.bus.i2c_rdwr( self._gyro_request, self._gyro_reader )
        x = int.from_bytes(self._gyro_reader.buf[0]+self._gyro_reader.buf[1], 'big', signed=True) * self._scaling_factor
        y = int.from_bytes(self._gyro_reader.buf[2]+self._gyro_reader.buf[3], 'big', signed=True) * self._scaling_factor
        z = int.from_bytes(self._gyro_reader.buf[4]+self._gyro_reader.buf[5], 'big', signed=True) * self._scaling_factor
        return (x, y, z) 
    
    @property
    def get_reader(self):
        return self._gyro_reader