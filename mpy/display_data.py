from m5stack import *
from m5ui import *
from mpu6050 import MPU6050
from mag3110 import MAG3110
import i2c_bus
clear_bg(0x111111)

itwoc = i2c_bus.get(i2c_bus.M_BUS)
mag = MAG3110(itwoc)
imu = MPU6050(itwoc)
btnA = M5Button(name='ButtonA', text='ButtonA', visibility=False)
btnB = M5Button(name='ButtonB', text='ButtonB', visibility=False)
btnC = M5Button(name='ButtonC', text='ButtonC', visibility=False)

labelx = M5TextBox(40, 30, "Text", lcd.FONT_Default, 0xFFFFFF)
labely = M5TextBox(40, 50, "Text", lcd.FONT_Default, 0xFFFFFF)
labelz = M5TextBox(40, 70, "Text", lcd.FONT_Default, 0xFFFFFF)
labelax = M5TextBox(40, 90, "Text", lcd.FONT_Default, 0xFFFFFF)
labelay = M5TextBox(40, 110, "Text", lcd.FONT_Default, 0xFFFFFF)
labelaz = M5TextBox(40, 130, "Text", lcd.FONT_Default, 0xFFFFFF)
labelgx = M5TextBox(40, 150, "Text", lcd.FONT_Default, 0xFFFFFF)
labelgy = M5TextBox(40, 170, "Text", lcd.FONT_Default, 0xFFFFFF)
labelgz = M5TextBox(40, 190, "Text", lcd.FONT_Default, 0xFFFFFF)
labelmg = M5TextBox(40, 210, "Text", lcd.FONT_Default, 0xFFFFFF)

lpitch = M5TextBox(5, 30, "pitch", lcd.FONT_Default, 0xFFFFFF)
lroll = M5TextBox(5, 50, "roll", lcd.FONT_Default, 0xFFFFFF)
lyaw = M5TextBox(5, 70, "yaw", lcd.FONT_Default, 0xFFFFFF)
lax = M5TextBox(5, 90, "ax", lcd.FONT_Default, 0xFFFFFF)
lay = M5TextBox(5, 110, "ay", lcd.FONT_Default, 0xFFFFFF)
laz = M5TextBox(5, 130, "az", lcd.FONT_Default, 0xFFFFFF)
lgx = M5TextBox(5, 150, "gx", lcd.FONT_Default, 0xFFFFFF)
lgy = M5TextBox(5, 170, "gy", lcd.FONT_Default, 0xFFFFFF)
lgz = M5TextBox(5, 190, "gz", lcd.FONT_Default, 0xFFFFFF)
lmg = M5TextBox(5, 210, "mag", lcd.FONT_Default, 0xFFFFFF)

gxo = 0
gyo = 0
gzo = 0

def calibrate():
  global imu, gxo, gyo, gzo
  wait(3)
  tx = 0
  ty = 0
  tz = 0
  
  for i in range(2000):
    x, y, z = imu.gyro
    tx += x
    ty += y
    tz += z

  gxo = tx / 2000
  gyo = ty / 2000
  gzo = tz / 2000
  imu.setGyroOffsets(gxo, gyo, gzo)
  
calibrate()

while True:
  labelx.setText(str(imu.ypr[1]))
  labely.setText(str(imu.ypr[2]))
  labelz.setText(str(imu.ypr[0]))
  ax, ay, az = imu.acceleration
  labelax.setText(str(ax))
  labelay.setText(str(ay))
  labelaz.setText(str(az))
  gx, gy, gz = imu.gyro
  gx -= gxo
  gy -= gyo
  gz -= gzo
  labelgx.setText(str(gx))
  labelgy.setText(str(gy))
  labelgz.setText(str(gz))
  labelmg.setText(str(mag.readMag()))
  wait(0.5)
