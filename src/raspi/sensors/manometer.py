import time
import smbus2

class PressureSensor():
    def __init__(self, bus, address=0x18, psi_range=(0, 25)):
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
        assert(psi_range[0] <= psi_range[1])
        self.psi_range = psi_range
        self.bus = bus
        self.ADDR = address

        self._REG_DATA = 0xAA
        
        # create some simple lambdas to shorthand reading and writing messages
        read = lambda x: smbus2.i2c_msg.read(self.ADDR, x)
        write = lambda x: smbus2.i2c_msg.write(self.ADDR, x)
        
        # set up the reader for all future readings
        self._psi_request = write( [ self._REG_DATA, 0x00, 0x00 ] )
        self._status_reader = read( 1 )
        self._psi_reader = read( 4 )
    
    def read(self):
        """Gets a reading from the gyroscope sensor for x, y, z

        Returns:
            (int, int, int): returns (x, y, z) taken from the gyroscope sensor as a signed number in degrees.
        """
        self.bus.i2c_rdwr( self._psi_request )
        time.sleep(0.1)

        done = False
        # set up timeout
        start = time.time()
        while not done:
            self.bus.i2c_rdwr( self._status_reader )
            # if status byte = completed or timeout
            if int.from_bytes(self._status_reader.buf[0],'big') == 0x40:
                done = True
            if (time.time() - start) > 1.0:
                raise RuntimeError("Reading taking too long to complete")

        # get actual reading and convert to psi
        self.bus.i2c_rdwr( self._psi_reader )
        print(self._psi_reader.buf[1]+self._psi_reader.buf[2]+self._psi_reader.buf[3])
        reading = int.from_bytes( self._psi_reader.buf[1]+self._psi_reader.buf[2]+self._psi_reader.buf[3], 'big' )
        psi = ((reading - 1677722) * (self.psi_range[1] - self.psi_range[0]) / 13421772) + self.psi_range[0]
        return psi

    def readPascal (self):
        return (self.read * 6894.76)