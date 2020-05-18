# Pioneer600 HAT project

This is a project that uses multiple modules being called into a main program to test the various features on the Pioneer600 HAT.

Monitoring : 

  * Time / Date 
  * BMP280 infos - Temperature & Pressure
  * Raspberry Pi Info 
	- CPU Temperature 
	- RAM Usage
	- CPU Usage
	- Disk Usage
  * IP Adresses 
  * Digital Output and Analog Input
  * 1-Wire Temperature sensor
  * System Command
	- Close this application
	- Restart Raspberry Pi
	- Shutdown system
	- Application Update (app-get update and upgrade)
	- Raspberry Pi Kernel Upgrade rpi-update
	- Close App
  * Serial Interface
  * Joystick Interface
  * OLED

Note: Open Pioneer600.py and review all packages called out. Update your Pi with the applicable items; load what you are missing.
