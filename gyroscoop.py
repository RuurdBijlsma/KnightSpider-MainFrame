import smbus

import math

import utils


class Gyroscoop(object):
    # Replace with value read via ic2detect
    ADDRESS = 0x68

    POWER_MGMT_1 = 0x6b
    POWER_MGMT_2 = 0x6c

    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47

    ACCEL_X = 0x3b
    ACCEL_Y = 0x3d
    ACCEL_Z = 0x3f

    ACCEL_SCALE_MAGIC = 16384.0

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.ADDRESS, self.POWER_MGMT_1, 1)

    def read_gyro(self):
        x = self.read_word_2c(self.GYRO_X)
        y = self.read_word_2c(self.GYRO_Y)
        z = self.read_word_2c(self.GYRO_Z)
        return (x,y,z)

    def read_accel(self):
        x = self.read_word_2c(self.ACCEL_X)
        y = self.read_word_2c(self.ACCEL_Y)
        z = self.read_word_2c(self.ACCEL_Z)
        return (x,y,z)

    def read_accel_scaled(self):
        x,y,z = self.read_accel()
        return (
            x / self.ACCEL_SCALE_MAGIC,
            y / self.ACCEL_SCALE_MAGIC,
            z / self.ACCEL_SCALE_MAGIC
        )


    def read_byte(self, adr):
        return self.bus.read_byte_data(self.ADDRESS, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.ADDRESS, adr)
        low = self.bus.read_byte_data(self.ADDRESS, adr + 1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val


    @staticmethod
    def get_y_rotation(rotation):
        x,y,z = rotation
        radians = math.atan2(x, utils.dist(y, z))
        return -math.degrees(radians)

    @staticmethod
    def get_x_rotation(rotation):
        x,y,z = rotation
        radians = math.atan2(y, utils.dist(x, z))
        return math.degrees(radians)