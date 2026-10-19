#!/usr/bin/env python
# Inspired by https://docs.circuitpython.org/projects/blinka/en/latest/examples.html  file pi_busio_i2c.py
import struct
import time
import sys
import board
import busio

# Addresses and offsets from Pimoroni code
# https://github.com/pimoroni/icm20948-python
ICM20948_ADDRS = [ 0x68, 0x69 ]
ICM20948_TEMP_OUT_H = 0x39
ICM20948_TEMP_OUT_L = 0x3A
# Offset and sensitivity - defined in electrical characteristics, and TEMP_OUT_H/L of datasheet
ICM20948_TEMPERATURE_DEGREES_OFFSET = 21
ICM20948_TEMPERATURE_SENSITIVITY = 333.87
ICM20948_ROOM_TEMP_OFFSET = 21


print("Blinka ICM-20948/29048 temperature measurement")
i2c = busio.I2C(board.SCL, board.SDA)
i2c_devices = i2c.scan()
print("I2C devices found:", [hex(i) for i in i2c_devices])

i2c_overlap = list(set(i2c_devices) & set(ICM20948_ADDRS))
imu_addr = ICM20948_ADDRS[0]  #sensible default

if len(i2c_overlap) > 1:
    print("Warning, multiple devices!  Using the first one.")
if len(i2c_overlap) > 0:
    imu_addr = i2c_overlap[0]
    print("Connecting to: ", hex(imu_addr))
else:
    print("Did not find the ICM-20948")
    sys.exit()

def temp_c(data):
    temp_raw = struct.unpack('>h', bytearray(data))[0]
    # Temperature calculations from
    # https://github.com/pimoroni/icm20948-python
    temperature_deg_c = ((temp_raw - ICM20948_ROOM_TEMP_OFFSET) / ICM20948_TEMPERATURE_SENSITIVITY) + ICM20948_TEMPERATURE_DEGREES_OFFSET
    return(temperature_deg_c)


while True:
    i2c.writeto(imu_addr, bytes([ICM20948_TEMP_OUT_H])),
    result = bytearray(2)
    i2c.readfrom_into(imu_addr, result)
    temp = temp_c(result)
    print(f"Temperature {temp} degrees C")
    time.sleep(0.5)
        
