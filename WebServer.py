#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import random
import time
import sys

SERVER_ADDRESS = '127.0.0.1'
MAX_CONNECTIONS = 2
FIXED_PORT = False


def handleRequest(tcpSocket):
	# 1. Receive request message from the client on connection socket
	# 2. Extract the path of the requested object from the message (second part of the HTTP header)
	# 3. Read the corresponding file from disk
	# 4. Store in temporary buffer
	# 5. Send the correct HTTP response error
	# 6. Send the content of the file to the socket
	# 7. Close the connection socket 
	return 200

def startServer(serverAddress, serverPort):
	# 1. Create server socket
	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 2. Bind the server socket to server address and server port
	tcpSocket.bind((serverAddress, serverPort))

	# 3. Continuously listen for connections to server socket
	tcpSocket.listen(MAX_CONNECTIONS)
	started = time.time()
	print 'Listening on ' + str(serverAddress) + ' | PORT: ' + str(serverPort) + '\n'

	while True:
		connection, extra = tcpSocket.accept()
		# Handle request if connection is accepted
		if (connection):
			print 'Connected - HANDLING REQUEST\n'
			print connection
			print extra
			status = handleRequest(tcpSocket)
			
			# Close server if request is satisfied
			if (status == 200):
				print 'Request Satisfied - CLOSING SERVER\n'
				tcpSocket.close()
				break
	
	# Useful info
	ranFor = time.time() - started
	print 'Server ran for: ' + '%.3f' % ranFor + ' seconds.'


# Takes user input, if user skips then port set to random
def userInput():
	print '>>> Enter the PORT number\n>>> Press ENTER to skip\n'
	# userInput = raw_input()
	userInput = None
	
	# Determine whether port is fixed or random 
	if (FIXED_PORT): port = 8080
	else: port = random.uniform(1025, 10000)

	if (userInput):
		# Only accept if port is higher than 1024
		if (int(userInput) > 1024): port = userInput
		else: 
			print 'Port number must be higher than 1024'
			quit()
	# Set port value if skipped
	else: print '! SKIPPING: Setting PORT to ' + str(port) + '\n'

	return int(port)


def main():
	port = userInput()
	startServer(SERVER_ADDRESS, port)


if __name__ == "__main__":
	main()