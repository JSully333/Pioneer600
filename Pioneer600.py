#!/usr/bin/python
# -*- coding:utf-8 -*-
# JSully333
# 2020
#
# This program is to allow the user to interface with each of the seperate functions of the Pioneer600 HAT.
# Where applicable, various modules that this program calls were configured to run as a stand-alone
# program, for troubleshooting and development, and to be called for use in this main program as needed.
# This program is given as Free License to users of GitHub. I present the Software as-is and
# I make no garantees or claims to its functionality or performance.
#
# In addition to this program and its associated modules you will need to set up your Raspberry Pi
# with the proper Raspberry Pi modules. Ensure you select the appropriate configuration
# in the Configuration Menu.


import RPi.GPIO as GPIO
import smbus
import spidev as SPI
import SSD1306
import time
from BMP280 import BMP280
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import fcntl
import struct
import add_module
from DovizKurlari import DovizKurlari
import PCF8591 as ADC #This is your Analog to Digital converter.
import ds18b20 as OneWire #Must have the ds18b20 1-Wire sensor plugged in
import ds3231 as RTC #Must have the ds3231 RTC enabled to get the temperature from it
import sys
import serial
import irm_Module as IRM # Remote Control input; MP3, 21 button remote.
import USB2UART_Module as USB2UART #Ensure your Raspberry Pi Configuration is set to Serial Port, not Serial Console.
import io #This is needed for the terminal input keyboard buffer clearing.

KEY = 20
address = 0x20
main_menu = 1
submenu = 1

Address = 0x48 #PCF8591 address
ADC.setup(Address)

DAC0_status = 0

ser = serial.Serial("/dev/ttyS0",115200,timeout=1) #This is the Serial configuration for the UART Test


def beep_on():
        bus.write_byte(address,0x7F&bus.read_byte(address))
def beep_off():
        bus.write_byte(address,0x80|bus.read_byte(address))
def led_off():
        bus.write_byte(address,0x10|bus.read_byte(address))
def led_on():
        bus.write_byte(address,0xEF&bus.read_byte(address))

def oled(bir,iki,ucst=""):
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),str(bir), font=font1, fill=255)
        draw.text((x, top+20),str(iki), font=font2, fill=255)
        draw.text((x, top+40),str(ucst), font=font2, fill=255)
        disp.image(image)
        disp.display()


def flush_input(): #This is to flush the keyboard buffer
        f = io.open("/dev/ttyS0") #This is tied to the value for the Serial configuration.
        flush_kb_buff = f.readline().strip() #This was 'print', before 'flush_kb_buff'.
        #The use of the 'print' function is not needed, unless for test purposes.


def menu ():
        global direction
        global submenu
        global main_menu
        global DAC0_status


        if direction == "up" :
                submenu = submenu - 1
        elif direction == 'down' :
                submenu =  submenu + 1
        elif direction == "right" :
                main_menu = main_menu + 1
                submenu = 1
        elif direction == "left" :
                main_menu = main_menu -1
                submenu = 1

        if main_menu == 12:
                main_menu = 1
        if main_menu == 0:
                main_menu = 11



        temp,pressure = bmp.get_temperature_and_pressure() #BMP280 code line


        #Information
        if main_menu == 1 :
                Temp_C,Temp_F = RTC.getTemp() #ds3231 code line

                if submenu == 4:
                        submenu = 1
                if submenu ==0:
                        submenu =3

                if submenu == 1:
                        oled("<  1.Time   >",time.strftime('%X'))
                if submenu == 2 :
                        oled("<  1.Date   >",time.strftime('%x'))
                elif submenu == 3 :
                        oled("<  1.RTC Temp >",(str(round(Temp_C,2))+" C"),(str(round(Temp_F,2))+" F"))

        # Sensor data
        elif main_menu == 2 :

                if submenu == 3:
                        submenu = 1
                if submenu ==0:
                        submenu =2

                if submenu ==1:
                        oled("< 2. BMP280 >","Temperature",(str(round(temp,2))+" C"))
                elif submenu ==2:
                        oled("< 2. BMP280 >","Pressure",round(pressure,2))

        # Device info
        elif main_menu == 3:

                if submenu == 5:
                        submenu = 1
                if submenu ==0:
                        submenu =4

                if submenu == 1 :
                        oled("< 3.Rpi Info >","CPU Temperature=",(add_module.getCPUtemperature()+" C"))
                elif submenu == 2 :
                        oled("< 3.Rpi Info >","Free RAM",(str(int(add_module.getRAMinfo()[2])/1024)+" MB"))
                elif submenu == 3 :
                        oled("< 3.Rpi Info >","CPU Usage",(str(add_module.getCPUuse())+" %"))
                elif submenu == 4 :
                        oled("< 3.Rpi Info >","Disk Usage",add_module.getDiskSpace()[3])
        # IP Address
        elif main_menu == 4 :

                if submenu == 3:
                        submenu = 1
                if submenu == 0:
                        submenu = 2

                if submenu == 1 :
                        oled("< 4. Rpi IP's >","WLAN0",add_module.get_ip_address('wlan0'))
                elif submenu == 2 :
                        oled("< 4. Rpi IP's >","ETH0",add_module.get_ip_address('eth0'))


        #Finance
        elif main_menu == 5 :

                if submenu == 3:
                        submenu = 1
                if submenu ==0:
                        submenu =2

                if submenu == 1 :
                        oled("< 5. Exch Rate >","Dolar / TL",DovizKurlari().DegerSor("USD",4))
                elif submenu == 2 :
                        oled("< 5. Exch Rate >","Euro / TL",DovizKurlari().DegerSor("EUR",4))


        #DAC0, LED1, and ADC0 through ADC3
        elif main_menu == 6 :

                if submenu == 6:
                        submenu = 1
                if submenu ==0:
                        submenu = 5

                if submenu == 1 :
                        oled("< 6. DAC0/LED1 >","Turn On/OFF","Press Button")
                        if GPIO.input(KEY) == 0:
                                if DAC0_status == 0:
                                        GPIO.output(LED1,GPIO.HIGH) #Turns on LED1 to indicate DAC0 is on
                                        ADC.write(255) #Turns on DAC0
                                        DAC0_status = 1
                                        time.sleep(.25)
                                else:
                                        GPIO.output(LED1,GPIO.LOW) #Turns off LED1 to indicate DAC0 is off
                                        ADC.write(0) #Turns off DAC0
                                        DAC0_status = 0
                                        time.sleep(.25)

                elif submenu == 2 :
                        oled("< 6. DAC0/LED1 >","Ain0",(str(round(ADC.read(0),2))+" Volts")) #PCF8591 code line

                elif submenu == 3 :
                        oled("< 6. DAC0/LED1 >","Ain1",(str(round(ADC.read(1),2))+" Volts")) #PCF8591 code line

                elif submenu == 4 :
                        oled("< 6. DAC0/LED1 >","Ain2",(str(round(ADC.read(2),2))+" Volts")) #PCF8591 code line

                elif submenu == 5 :
                        oled("< 6. DAC0/LED1 >","Ain3",(str(round(ADC.read(3),2))+" Volts")) #PCF8591 code line




        #System
        elif main_menu == 7 :

                if submenu == 5:
                        submenu = 1
                if submenu ==0:
                        submenu =4

                elif submenu == 1 :
                        oled("< 7. System >","Close App","Press Button")
                        if GPIO.input(KEY) == 0:
                                sys.exit()
                elif submenu == 2 :
                        oled("< 7. System >","Restart","Press Button")
                        if GPIO.input(KEY) == 0:
                                os.popen('sudo reboot')
                elif submenu == 3 :
                        oled("< 7. System >","Halt System","Press Button")
                        if GPIO.input(KEY) == 0:
                                os.popen('sudo halt')
                elif submenu == 4 :
                        oled("< 7. System >","App Update","Press Button")
                        if GPIO.input(KEY) == 0:
                                oled("< 7. System >","Update ...")
                                os.popen('sudo apt-get update')
                                oled("< 7. System >","Upgrade ...")
                                os.popen('sudo apt-get upgrade -y')
                                oled("< 7. System >","Completed")



        #Additional sensors
        elif main_menu == 8 :
                temp_c,temp_f = OneWire.read_temp() #ds18b20 code line
                f = OneWire.read_rom() #ds18b20 code line

                if submenu == 3:
                        submenu = 1
                if submenu ==0:
                        submenu =2

                if submenu ==1:
                        oled("< 8. Sensors >",f,(str(round(temp_c,2))+" C"))
                elif submenu ==2:
                        oled("< 8. Sensors >",f,(str(round(temp_f,2))+" F"))

        # IRM readings
        elif main_menu == 9 :

                if submenu == 2:
                        submenu = 1
                if submenu ==0:
                        submenu =1

                if submenu ==1:
                        IRM_key = IRM.irm_key()
                        oled("< 9. IRM >","Readings",IRM_key) #This is not catching all the button presses.
                        #The issue is the structure of this program would need to change to handle the timing.
                        #Running a thread does not improve program response to sensor input. To improve the
                        #response to the sensor input the program needs to be restructured/shortened.



        #USB2UART TX Test
        elif main_menu == 10 :
                oled("< 10. USB2UART >","Run TX test","Press Button") #This is to test the transmission from the Pi to a PC.
                if GPIO.input(KEY) == 0:
                        ser.write("Test line\r\n".encode())
                        oled("< 10. USB2UART >","Test line sent","View results")
                        time.sleep(2)

        #USB2UART RX Test
        elif main_menu == 11 :
                oled("< 11. USB2UART >","Run RX test","Press Button") #This is to test the
                #transmission from the PC to a Pi. No more than a small word, due to the OLED size.
                if GPIO.input(KEY) == 0:
                        flush_input() #Calls the function to clear the
                        #terminal keyboard buffer before the desired input is collected.
                        oled("< 11. USB2UART >","Button Pressed","Starting test")
                        ser.write("Type something\r\n".encode())
                        out = USB2UART.readData()
                        oled("< 11. USB2UART >","You wrote:",str(out))
                        ser.write("You wrote: ".encode() + str(out).encode() + "\r\n".encode())
                        time.sleep(2)


        else :
                print ("something went wrong")

        return (submenu)

# Raspberry Pi pin configuration:
RST = 19
LED1 = 26
global PIN
PIN = 18

# Note the following are only used with SPI:
DC = 16
bus = 0
device = 0

# 128x64 display with hardware SPI:
disp = SSD1306.SSD1306(RST, DC, SPI.SpiDev(bus,device))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Load image based on OLED display height.  Note that image is converted to 1 bit color.
imageOpen = Image.open(os.path.dirname(os.path.realpath(__file__)) +"/pioneer600.bmp").convert('1')
#imageClose = Image.open(os.path.dirname(os.path.realpath(__file__)) +"/pioneer600_close.bmp").convert('1') #Commented out on 10122018 to eliminate pictures being used for this program.

# Alternatively load a different format image, resize it, and convert to 1 bit color.
#image = Image.open('happycat.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')

# Display image.
disp.image(imageOpen)
disp.display()

time.sleep(2)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 1
top = padding
x = padding
# Load default font.
# font = ImageFont.load_default()
font_dir =  os.path.dirname(os.path.realpath(__file__)) +"/KeepCalm-Medium.ttf"
font1 = ImageFont.truetype(font_dir, 15)
font2 = ImageFont.truetype(font_dir, 14)

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(LED1,GPIO.OUT)
GPIO.output(LED1,GPIO.LOW)
GPIO.setup(PIN,GPIO.IN,GPIO.PUD_UP)

bmp = BMP280()
bus = smbus.SMBus(1)

print("Pioneer600 Test Program !!!")
print("Revision Number 1")

try:
        while True:

                bus.write_byte(address,0x0F|bus.read_byte(address))
                value = bus.read_byte(address) | 0xF0
                if value != 0xFF:
                        led_on()
                        #beep_on()
                        if (value | 0xFE) != 0xFF:
                                direction="left"
                        elif (value | 0xFD) != 0xFF:
                                direction="up"
                        elif (value | 0xFB) != 0xFF:
                                direction="down"
                        else :
                                direction="right"
                        while value != 0xFF:
                                bus.write_byte(address,0x0F|bus.read_byte(address))
                                value = bus.read_byte(address) | 0xF0
                                time.sleep(0.01)
                        led_off()
                        #beep_off()
                        submenu=menu()

                time.sleep(0.1)
                direction="clear"
                submenu=menu()

# for keyboard interrupt
except (KeyboardInterrupt, SystemExit):
        print ("Keyboard Interrupt or System Exit")
        oled("Keyboard","Interrupt or","System Exit")
        #time.sleep(2)
        # Clear display.
        #disp.image(imageClose) #Commented out to eliminate pictures being used for this program.
        #disp.display() #Commented out to eliminate pictures being used for this program.

        time.sleep(2)
        disp.clear()
        disp.display()
        GPIO.cleanup();

except Exception as e:
        print ("ERROR")
        # Clear display.
        oled("Error",e,"Error")
        print(e)
        #time.sleep(2)
        #disp.image(imageClose) #Commented out to eliminate pictures being used for this program.
        #disp.display() #Commented out to eliminate pictures being used for this program.

        time.sleep(2)
        disp.clear()
        disp.display()
        GPIO.cleanup();
