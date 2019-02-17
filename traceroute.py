#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 64

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

# Traces the route of a host
def traceroute(host):
    destinationAddress = socket.gethostbyname(host)
    for ttl in range(1, MAX_HOPS):
        # Create socket
        icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        icmpSocket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        # Build packet
        ID = os.getpid()
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, ID, 1)
        data = struct.pack('c', '*')
        checksumValue = checksum(header + data)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, checksumValue, ID, 1)

        icmpSocket.sendto(header + data, (destinationAddress, 80))




# Takes user input and passes it to the traceroute function
def userInput():
    userInput = raw_input()
    arguments = len(userInput.split())

    # Trace host using default values
    if arguments == 2:
        if "traceroute" in userInput:
            operation, host = userInput.split()
            # traceroute(host)
            print(host)

traceroute('lancaster.ac.uk')