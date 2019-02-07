#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import os
import sys
import struct
import time
import select
import binascii  


ICMP_ECHO_REQUEST = 8 #ICMP type code for echo request messages
ICMP_ECHO_REPLY = 0 #ICMP type code for echo reply messages


def checksum(string): 
	csum = 0
	countTo = (len(string) // 2) * 2  
	count = 0

	while count < countTo:
		thisVal = ord(string[count+1]) * 256 + ord(string[count]) 
		csum = csum + thisVal 
		csum = csum & 0xffffffff  
		count = count + 2
	
	if countTo < len(string):
		csum = csum + ord(string[len(string) - 1])
		csum = csum & 0xffffffff 
	
	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum 
	answer = answer & 0xffff 
	answer = answer >> 8 | (answer << 8 & 0xff00)
	
	if sys.platform == 'darwin':
		answer = htons(answer) & 0xffff		
	else:
		answer = htons(answer)

	return answer 
	
def receiveOnePing(icmpSocket, destinationAddress, ID, timeout):
	# 1. Wait for the socket to receive a reply
	# 2. Once received, record time of receipt, otherwise, handle a timeout
	# 3. Compare the time of receipt to time of sending, producing the total network delay
	# 4. Unpack the packet header for useful information, including the ID
	# 5. Check that the ID matches between the request and reply
	# 6. Return total network delay
	pass # Remove/replace when function is complete
	
def sendOnePing(icmpSocket, destinationAddress, ID):
	# 1. Build ICMP header
	# 2. Checksum ICMP packet using given function
	# 3. Insert checksum into packet
	# 4. Send packet using socket
	# 5. Record time of sending
	struct.pack('@hh')

	
def doOnePing(destinationAddress, timeout): 
	# 1. Create ICMP socket
	# 2. Call sendOnePing function
	# 3. Call receiveOnePing function
	# 4. Close ICMP socket
	# 5. Return total network delay
	pass
	
def ping(host, count=10, timeout=0.1):
	# 1. Look up hostname, resolving it to an IP address
	# 2. Call doOnePing function, approximately every second
	# 3. Print out the returned delay
	# 4. Continue this process until stopped
	hostAddress = socket.gethostbyname(host)
	i = 1
	while i < count:
		doOnePing(hostAddress, timeout)
		time.sleep(timeout)
		print hostAddress



# User input
userInput = raw_input()
arguments = len(userInput.split())

# Ping host fixed number of times
if arguments == 2:
	if "ping" in userInput:
		operation, host = userInput.split()
		ping(host)

# Ping host specified number of times
elif arguments == 4:
	if "-c" in userInput:
		operation, host, option, count = userInput.split()
		ping(host, count)

# Operation not recognised
else:
	print "Invalid Operation"























