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
		answer = socket.htons(answer) & 0xffff		
	else:
		answer = socket.htons(answer)

	return answer


	
def receiveOnePing(icmpSocket, destinationAddress, ID, timeout):
	# Wait for receipt and record time
	networkDelay = 0
	while True:
		packetReceived = select.select([icmpSocket], [], [], timeout) # Only need to read
		
		# Handle timeout
		if (packetReceived[0] == []):
			print 'TIMEOUT'
		else:
			# Record time
			receiptTime = time.time()

			# Unpack packet header for useful information
			packet = icmpSocket.recv(64)
			header = packet[20:28]
			typ, code, checksum, identifier, seq = struct.unpack('bbHHh', header)

			# Check that the ID matches between the request and reply
			if (ID == identifier):
				return receiptTime
			else:
				print 'ID match failed'


	
def sendOnePing(icmpSocket, destinationAddress, ID, sequence):
	# Build ICMP header
	header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, ID, sequence)

	# Checksum ICMP packet using given function
	checksumValue = checksum(header)
	
	# Insert checksum into packet
	header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, checksumValue, ID, sequence)

	# Send packet using socket
	icmpSocket.sendto(header, (destinationAddress, 80))

	# Record time of sending
	timeSent = time.time()
	return timeSent

	

def doOnePing(destinationAddress, timeout, sequence): 
	# Create ICMP socket
	icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))

	# Call sendOnePing function
	ID = os.getpid()
	timeSent = sendOnePing(icmpSocket, destinationAddress, ID, sequence)

	# Call receiveOnePing function
	timeReceived = receiveOnePing(icmpSocket, destinationAddress, ID, timeout)

	# Close ICMP socket
	icmpSocket.close()

	# Return total network delay
	return timeReceived - timeSent

	

def ping(host, count=10, timeout=1):
	# Look up hostname, resolving it to an IP address
	hostAddress = socket.gethostbyname(host)
	

	# Send one ping every 1000 ms
	count = int(count);
	counter = 1
	while counter <= count:		
		# Print delay
		networkDelay = doOnePing(hostAddress, timeout, counter)
		formattedDelay = '%.3f' % (networkDelay * 1000) + ' ms'
		print '64 bytes from ' + str(hostAddress) + ': icmp_seq=' + str(counter) + ' time=' + str(formattedDelay)

		# Delay for timeout ms
		time.sleep(timeout)
		counter += 1



def userInput():
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


userInput()



















