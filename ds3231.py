#!/usr/bin/python
# -*- coding:utf-8 -*-
import smbus
import os
import time

bus = smbus.SMBus(1)
address = 0x68


def getTemp():
   os.system('sudo rmmod rtc_ds1307')
   byte_tmsb = bus.read_byte_data(address,0x11)
   byte_tlsb = bin(bus.read_byte_data(address,0x12))[2:].zfill(8)
   Temp_C = byte_tmsb+int(byte_tlsb[0])*2**(-1)+int(byte_tlsb[1])*2**(-2)
   Temp_F = Temp_C * 9.0 / 5.0 + 32.0
   os.system('sudo modprobe rtc_ds1307')
   return Temp_C, Temp_F



if __name__ == "__main__":
   while True:
      print(' C=%3.3f  F=%3.3f'% getTemp())
      time.sleep(1)
