from machine import I2C
from micropython import const
import ustruct, utime
import i2c_bus

_I2C_ADDRESS_MAG3110 = const(0x0e)
_I2C_ADDRESS_FXMS3110 = const(0x0f)

_DR_STATUS_R = const(0x00)
_OUT_X_MSB_R = const(0x01)
_OUT_X_LSB_R = const(0x02)
_OUT_Y_MSB_R = const(0x03)
_OUT_Y_LSB_R = const(0x04)
_OUT_Z_MSB_R = const(0x05)
_OUT_Z_LSB_R = const(0x06)
_WHO_AM_I_R = const(0x07)
_SYSMOD_R = const(0x08)
_OFF_X_MSB_RW = const(0x09)
_OFF_X_LSB_RW = const(0x0a)
_OFF_Y_MSB_RW = const(0x0b)
_OFF_Y_LSB_RW = const(0x0c)
_OFF_Z_MSB_RW = const(0x0d)
_OFF_Z_LSB_RW = const(0x0e)
_DIE_TEMP_R = const(0x0f)
_CTRL_REG1_RW = const(0x10)
_CTRL_REG2_RW = const(0x11)

# CTRL_REG1 SETTINGS
_CTRL_REG1_OS80_DR16 = const(0x00)
_CTRL_REG1_OS40_DR32 = const(0x08)
_CTRL_REG1_OS20_DR64 = const(0x10)
_CTRL_REG1_OS10_DR128 = const(0x18)
_CTRL_REG1_OS40_DR16 = const(0x20)
_CTRL_REG1_OS20_DR32 = const(0x28)
_CTRL_REG1_OS10_DR64 = const(0x30)
_CTRL_REG1_OS5_DR128 = const(0x38)
_CTRL_REG1_OS20_DR16 = const(0x40)
_CTRL_REG1_OS10_DR32 = const(0x48)
_CTRL_REG1_OS5_DR64 = const(0x50)
_CTRL_REG1_OS2_5_DR128 = const(0x58)
_CTRL_REG1_OS10_DR16 = const(0x60)
_CTRL_REG1_OS5_DR32 = const(0x68)
_CTRL_REG1_OS2_5_DR64 = const(0x70)
_CTRL_REG1_OS1_25_DR128 = const(0x78)
_CTRL_REG1_OS5_DR16 = const(0x80)
_CTRL_REG1_OS2_5_DR32 = const(0x88)
_CTRL_REG1_OS1_25_DR64 = const(0x90)
_CTRL_REG1_OS0_63_DR128 = const(0x98)
_CTRL_REG1_OS2_5_DR16 = const(0xa0)
_CTRL_REG1_OS1_25_DR32 = const(0xa8)
_CTRL_REG1_OS0_63_DR64 = const(0xb0)
_CTRL_REG1_OS0_31_DR128 = const(0xb8)
_CTRL_REG1_OS1_25_DR16 = const(0xc0)
_CTRL_REG1_OS0_63_DR32 = const(0xc8)
_CTRL_REG1_OS0_31_DR64 = const(0xd0)
_CTRL_REG1_OS0_16_DR128 = const(0xd8)
_CTRL_REG1_OS0_63_DR16 = const(0xe0)
_CTRL_REG1_OS0_31_DR32 = const(0xe8)
_CTRL_REG1_OS0_16_DR64 = const(0xf0)
_CTRL_REG1_OS0_08_DR128 = const(0xf8)

_CTRL_REG1_FAST_READ = const(0x04)
_CTRL_REG1_TRIGGER_MEASUREMENT = const(0x02)
_CTRL_REG1_ACTIVE_MODE = const(0x01)
_CTRL_REG1_STANDBY_MODE = const(0x00)

# CTRL_REG2 SETTINGS
_CTRL_REG2_AUTO_MRST_EN = const(0x80)  # Automatic Magnetic Sensor Reset.
_CTRL_REG2_RAW = const(0x20)  # Data output correction.
_CTRL_REG2_MAG_RST = const(0x10)  # Magnetic Sensor Reset (One-Shot).

class MAG3110:

    def __init__(self, i2c = None, i2cAddress=_I2C_ADDRESS_MAG3110):
        if i2c:
            self.i2c = i2c
        else:
            i2c = i2c_bus.get(i2c_bus.M_BUS)
            
        self.i2cAddress = i2cAddress
        self.__initialSetup()
        
    def __initialSetup(self):
        self.modeConfig()
        self.dataRateConfig()
        
    def dataRateConfig(self):
        dataRateSettings = ustruct.pack('<b', _CTRL_REG1_ACTIVE_MODE)
        self.i2c.writeto_mem(self.i2cAddress, _CTRL_REG1_RW, dataRateSettings)
        utime.sleep_ms(15)

    def modeConfig(self):
        mode = ustruct.pack('<b', _CTRL_REG2_AUTO_MRST_EN)
        self.i2c.writeto_mem(self.i2cAddress, _CTRL_REG2_RW, mode)
        utime.sleep_ms(15)
   
    def readMag(self):
        data6bytes = self.i2c.readfrom_mem(self.i2cAddress, _OUT_X_MSB_R, 6)
        return ustruct.unpack('>HHH', data6bytes)
        
        
