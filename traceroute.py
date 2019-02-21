#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 64
TRIES = 3
BYTES = 52

def main():
    userInput()


# Takes user input and passes it to the traceroute function
def userInput():
    userInput = raw_input()
    arguments = len(userInput.split())

    # Trace host using default values
    if arguments == 2:
        if "traceroute" in userInput:
            operation, host = userInput.split()
            traceroute(host)
    
    # Trace host using custom timeout
    elif arguments == 4:
        if "-t" in userInput:
            operation, host, option, timeout = userInput.split()
            traceroute(host, int(timeout))
    else: print "Invalid Operation"


# Traces the route of a host
def traceroute(host, timeout=0):
    # Get address info
    hostname, aliaslist, ipaddrlist = socket.gethostbyname_ex(host)
    print 'traceroute to ' + hostname + ' (' + str(ipaddrlist[0]) + '), ' + str(MAX_HOPS) + ' hops max, ' + str(BYTES) + ' byte packets'

    # Loop until request type is 0 or the number of max hop is exceeded
    for ttl in range(1, MAX_HOPS + 1):
        # Loop until packet recevied or the number of tries exceeded
        for attempt in range(TRIES):
            # Create socket
            icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
            icmpSocket.setsockopt(socket.SOL_IP, socket.IP_TTL, struct.pack('I', ttl))

            # Build packet with data
            ID = os.getpid()
            header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, ID, 1)
            data = struct.pack('c', '*')
            checksumValue = checksum(header + data)
            header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, checksumValue, ID, 1)
        
            # Send packet and note time
            icmpSocket.sendto(header + data, (ipaddrlist[0], timeout))
            timeSent = time.time()
            
            # Attempt to receive packet    
            packetReceived = select.select([icmpSocket], [], [], 1) # Only need to read
            if packetReceived[0] == []: print '*'
            else:
                packet, address = icmpSocket.recvfrom(BYTES)
                timeReceived = time.time()
                recv_header = packet[20:28]
                break

        # Extract info from header
        request, code, checksum_val, identifier, seq = struct.unpack('bbHHh', recv_header)
        
        # Print hop information
        nextHost = socket.getnameinfo(address, 0)[0]
        formattedDelay = '%.3f' % ((timeReceived - timeSent) * 1000) + ' ms'
        print ttl, nextHost, '(' + address[0] + ')', formattedDelay

        # Sleep for timeout time
        time.sleep(timeout)

        # Determine whether program will loop or exit
        if request == 0: break
            

# Completes a checksum opeartion on a given string
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


if __name__ == "__main__":
    main()