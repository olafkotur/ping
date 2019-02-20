#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys
import random
import time

SERVER_ADDRESS = '127.0.0.1'
MAX_CONNECTIONS = 4
FIXED_PORT = True


def handleRequest(tcpSocket):
	# Receive request message from the client on connection socket
	data = tcpSocket.recv(1024).decode()
	
	# Extract useful infromation for the HTTP header
	data = data.split(' ')
	request = data[1]
	print 'Client requested file ' + str(request) + ' from disk'

	# TESTING ONLY - shutdown server if request is close
	status = 200
	if (request == '/close'): status = 9999

	# 3. Read the corresponding file from disk
	# 4. Store in temporary buffer
	# 5. Send the correct HTTP response error
	# 6. Send the content of the file to the socket
	# 7. Close the connection socket 
	return status

def startServer(serverAddress, serverPort):
	# Create server socket
	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the server socket to server address and server port, increment until successful
	portBound = False
	while not portBound:
		try: 
			tcpSocket.bind((serverAddress, serverPort))
			portBound = True
		except:
			print 'PORT ' + str(serverPort - 1) + ' is already in use\nAttempting PORT ' + str(serverPort)
			serverPort += 1


	# Listen for connections to server socket
	tcpSocket.listen(MAX_CONNECTIONS)
	print 'Listening on ' + str(serverAddress) + ' | PORT: ' + str(serverPort) + '\n'
	startedTime = time.time()

	# Keep server running
	serverActive = True
	while serverActive:
		# Accept new connections
		connectionSocket, address = tcpSocket.accept()

		# Handle request if connection is accepted
		if (connectionSocket):
			print 'Received a connection at: ' + str(address[0]) + ' | ' + str(address[1]) + '\n'
			
			# Return status code from request
			status = handleRequest(connectionSocket)
			
			# Close server if request is satisfied
			if (status == 200):
				print 'Request Satisfied\n'
			elif (status == 404):
				print 'This is not the file you are looking for'
			elif (status == 9999): serverActive = False
	
	# Useful info
	tcpSocket.close()
	ranFor = time.time() - startedTime
	print '\nServer ran for: ' + '%.3f' % ranFor + ' seconds.'


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
	else: print '! SKIPPING: Setting PORT to ' + str(port)

	return int(port)

def main():
	port = userInput()
	startServer(SERVER_ADDRESS, port)


if __name__ == "__main__":
	main()