#!/usr/bin/python

"""gsm_controller module.

This module controls the GSM module (SIM900) interfaces via 
physical serial and GPIO ports on the single-board computer. 

"""

import serial
import time
import RPi.GPIO as GPIO
#from csv import reader
import re

GPIO.setmode(GPIO.BOARD)
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0)

# FORBID INCOMING CALLS
# AT+GSMBUSY=1
	
# SET COMMAND ECHO MODE OFF
# ATE0	

# SET RESULT CODE OFF
# ATQ1

# 
#

def power_toggle():
	"""Toggles the SIM900 GSM module ON or OFF.
	
	Powers ON or OFF the SIM900 GSM shield via GPIO pin
	on the RPi.
	
	Args: None.
	
	Returns: None.
	
	Raises: None.
	"""
	
	GPIO.setup(11, GPIO.OUT)
	GPIO.output(11, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(11, GPIO.LOW)
	
	return
	
def send_message(message, address):
	"""Sends an SMS message.
	
	Pushes an SMS message onto the cellular 
	network using physical serial interface on the RPi.
	
	Args: 
	message: String.
	address: String.
		
	Returns: None.
	
	Raises: None.
	"""
	if(ser.isOpen() == False):	# Check if serial is already open.
		ser.open()
	
	ser.write('AT+CMGS="+%s"\r' % address)	# Destination address
	ser.write("%s\r" % message) # Message
	ser.write(chr(26))	# End of text requires (^Z). 
	ser.close()
	
	return

def get_unread_messages():
	"""Retrieves unread messages.
	
	Queries the storage on the SIM card for 
	unread SMS messages received via the cellular network
	using physical serial interface on the RPi. 
	
	Args: None.
	
	Returns: 
	Message: String.
	Address: String.
	
	Raises: None.
	"""

	if(ser.isOpen() == False):
		ser.open()
	
	ser.reset_input_buffer()	
	
	ser.write('AT+CMGL="REC UNREAD"\r')	# Request all unread messages
	response = ser.read(size = ser.in_waiting) # Read all unread messages
	
	if (response):
		match = re.finditer("\+CMGL: (\d+),""(.+)"",""(.+)"",(.*),""(.+)""\n(.+)\n", response)
		for each in match:
			print match[0]
		
		#message_list = response.split('+CMGL: ')
		#for i in message_list:
			# message_parameters = list(reader(i))
			# message_index = message_parameters[0]
		

	
	return
	

def delete_read_messages():
	"""Deletes read messages.
	
	Deletes all stored SMS messages from the SIM
	card whose status is "received read" as well as 
	sent mobile originated numbers.
	
	Args: None.
	
	Returns: None.
	
	Raises: None.
	"""
	
	
	
	return
	
def power_reset():
	"""Resets the SIM900 module.
	
	Resets the SIM900 GSM shield via RPi GPIO pin.
	
	Args: None.
	
	Returns: None.
	
	Raises: None.
	"""
	
	GPIO.setup(12, GPIO.OUT)
	GPIO.output(12, GPIO.HIGH)
	time.sleep(2);
	GPIO.output(12, GPIO.LOW)
	
	return
	
def clean_up():
	"""Resets the GPIO pin states
	
	Resets the RPi GPIO pin states by
	calling the cleanup function in the GPIO lib.
	Only effective if called at END of program.
	
	Args: None.
	
	Returns: None.
	
	Raises: None.
	"""
	
	GPIO.cleanup()
	
	return
	
