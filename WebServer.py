#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys
import random
import time

SERVER_ADDRESS = '127.0.0.1'
MAX_CONNECTIONS = 4
FIXED_PORT = True


def main():
	port = userInput()
	startServer(SERVER_ADDRESS, port)

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


def startServer(serverAddress, serverPort):
	# Create server socket
	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the server socket to server address and server port, increment port until successful
	portBound = False
	while not portBound:
		try: 
			tcpSocket.bind((serverAddress, serverPort))
			portBound = True
		except:
			serverPort += 1
			print 'PORT ' + str(serverPort - 1) + ' is already in use, attempting to connect using PORT ' + str(serverPort)

	# Listen for connections to server socket
	tcpSocket.listen(MAX_CONNECTIONS)
	print 'Listening on ' + str(serverAddress) + ' | PORT: ' + str(serverPort) + '\n'
	startedTime = time.time()

	# Accept new connections
	connectionSocket, address = tcpSocket.accept()

	# Handle request if connection is accepted
	if (connectionSocket):
		print 'Received a connection at: ' + str(address[0]) + ' | ' + str(address[1])
		
		# Handle status code from client
		status = handleRequest(connectionSocket)
		if (status == 200): print '200 OK'
		elif (status == 404): print '404 Not Found\n'
	
	# Useful info
	tcpSocket.close()
	ranFor = time.time() - startedTime
	print '\nServer ran for: ' + '%.3f' % ranFor + ' seconds.'
	sys.exit()

def handleRequest(tcpSocket):
	# Receive request message from the client on connection socket
	data = tcpSocket.recv(1024).decode()
	
	# Extract useful infromation for the HTTP header
	print data
	data = data.split(' ')
	method, request = data[0], data[1]

	if (method == 'GET'):	
		# Set default file to index.html
		if (request == '/'): request = '/index.html'
		print 'Client requested file ' + str(request) + ' from disk\n'
		
		# Read the corresponding file from disk
		try: 
			# Grab the file
			file = open(request[1:], 'r')
			requestedData = file.read()
			file.close()
			
			# Pack the file into the header
			header = createHeader(' ' + str(200) + ' OK')
			requestedData = header + requestedData.encode()
			tcpSocket.send(requestedData)
			status = 200
		except:
			status = 404


	# 6. Send the content of the file to the sock8et
	# 7. Close the connection socket

	# TESTING ONLY - shutdown server if request is close
	if (request == '/close'): status = 9999
	
	return status


# Generates header according to the provided code
def createHeader(code):
	formattedTime = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
	header = 'HTTP/1.1 ' + code + '\n'
	header += 'Date: ' + formattedTime + '\n'
	header += 'Server: WebServer Example\n'
	print header
	print header.encode()
	return header.encode()


# Execute main
if __name__ == "__main__":
	main()