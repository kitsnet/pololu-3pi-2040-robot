from pololu_3pi_2040_robot import robot
import time
from machine import I2C, Pin
from vl6180x import Sensor

display = robot.Display()

class SensorInterface:
  def getSensorData(self, sensorId):
    sensor1 = Pin(27, Pin.OUT)
    sensor2 = Pin(28, Pin.OUT)
    sensor3 = Pin(29, Pin.OUT)

    sensor1.value(0) # turn off sensor 1
    sensor2.value(0) # turn off sensor 2
    sensor3.value(0) # turn off sensor 3
    time.sleep_ms(100)

    i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=400_000)
    sensor1.value(1) # turn on sensor 1
    time.sleep_ms(100)
    tof1 = Sensor(i2c)
    tof1.address(0x30)
    sensor2.value(1) # turn on sensor 2
    time.sleep_ms(100)
    tof2 = Sensor(i2c)
    tof2.address(0x31)
    sensor3.value(1) # turn on sensor 3
    time.sleep_ms(100)
    tof3 = Sensor(i2c)
    tof3.address(0x32)

    distance = 0
    display.fill(0)
    if sensorId == 1:
      distance = tof1.range()
      display.text(" Sensor1: " + str(distance), 0, 0)
      display.text(" Right wall " + str(distance), 0, 8)
    elif sensorId == 2:
      distance = tof2.range()
      display.text(" Sensor2: " + str(distance), 0, 0)
      display.text(" Front wall ", 0, 8)
    elif sensorId == 3:
      distance= tof3.range()
      display.text(" Sensor3: " + str(distance), 0, 0)
      display.text(" Left wall " + str(distance), 0, 8)
    display.show()
    return distance
