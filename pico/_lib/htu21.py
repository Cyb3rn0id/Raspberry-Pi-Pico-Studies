from machine import I2C
  
class HTU21:
    def __init__(self, i2c, address):
        self.i2c = i2c
        self.i2c_addr=address

    def _crc_check(self, value):
        #https://github.com/sparkfun/HTU21D_Breakout
        remainder = ((value[0] << 8) + value[1]) << 8
        remainder |= value[2]
        divsor = 0x988000

        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divsor
            divsor >>= 1

        if remainder == 0:
            return True
        else:
            return False

    def _measure(self, address):
       data = bytearray(3)
       self.i2c.writeto(self.i2c_addr, bytearray([address]))
       self.i2c.readfrom_into(self.i2c_addr, data)
       if not self._crc_check(data):
            raise ValueError()
       res = (data[0] << 8) + data[1]
       res &= 0xFFFC
       return res

    @property
    def temperature(self):
        res = self._measure(0xE3)
        return -46.85 + (175.72 * res / 65536)

    @property
    def humidity(self):
        res =  self._measure(0xE5)
        return -6 + (125.0 * res / 65536)
