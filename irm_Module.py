#!/usr/bin/python
# -*- coding:utf-8 -*-
#Code had been changed to work as a module for other programs also.
#Code is not complete, needs to be cleaned up, and needs to be tested!
import RPi.GPIO as GPIO
import time

global PIN
PIN = 18

def irm_key():
        try:
                while True:
                        if GPIO.input(PIN) == 0:
                                count = 0
                                while GPIO.input(PIN) == 0 and count < 200:  #9ms
                                        count += 1
                                        time.sleep(0.00006)

                                count = 0
                                while GPIO.input(PIN) == 1 and count < 80:  #4.5ms
                                        count += 1
                                        time.sleep(0.00006)

                                idx = 0
                                cnt = 0
                                data = [0,0,0,0]
                                for i in range(0,32):
                                        count = 0
                                        while GPIO.input(PIN) == 0 and count < 15:    #0.56ms
                                                count += 1
                                                time.sleep(0.00006)
                                
                                        count = 0
                                        while GPIO.input(PIN) == 1 and count < 40:   #0: 0.56mx
                                                count += 1                               #1: 1.69ms
                                                time.sleep(0.00006)
                                
                                        if count > 8:
                                                data[idx] |= 1<<cnt
                                        if cnt == 7:
                                                cnt = 0
                                                idx += 1
                                        else:
                                                cnt += 1
                                if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
                                        print("Get the key: 0x%02x" %data[2])
                                        return data[2]
                        else:
                                return -1

        except KeyboardInterrupt:
                GPIO.cleanup();



if __name__ == '__main__':
        import time
        PIN = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN,GPIO.IN,GPIO.PUD_UP)
        
        print('IRM Test Start ...\n')


        time.sleep(1)


        while True:

                temp = irm_key()
                #if temp == -1:
                        #print (irm_key()) #This is to test.
                        #time.sleep(0.5)
                #if temp != -1:
                        #print (irm_key()) #This may not be correct. Nor the line of code for return key.
                        #time.sleep(0.5)


