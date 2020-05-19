#!/usr/bin/python
# -*- coding:utf-8 -*-
#------------------------------------------------------
#
#		This is a program for USB2UART Module.
#
#------------------------------------------------------
import time
import serial

ser = serial.Serial("/dev/ttyS0",115200,timeout=1)

def readData():
    buffer = ""
    while True:
        oneByte = ser.read(1)
        if oneByte == b"\r":    #method should return bytes
            return buffer

        else:
            buffer += oneByte.decode("ascii")


if __name__ == "__main__":


    try:
        ser.write("\r\n".encode())
        while True:
            ser.write("Type something: ".encode())
            out = readData()
            ser.write("\r\nYou wrote: ".encode() + str(out).encode() + "\r\n".encode())



    # for keyboard interrupt
    except (KeyboardInterrupt, SystemExit):
            print ("Keyboard Interrupt or System Exit")


    except Exception as e:
            print ("ERROR", e)

