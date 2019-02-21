#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys

# These following libraries do not help with the core function of the task
# these were checked with the professor and were said to be ok for use
import random # Used to generate random port number
import time # Used to get current time for the HTTP header
import signal # Used to detect CTRL-C 


MAX_CONNECTIONS = 4		# Max number of refused connections
FIXED_PORT = True		# Always attempt to use PORT 8080 if available
TIMEOUT = 100			# Socket blocking value
SERVER_ADDRESS = '127.0.0.1'
AVAILABLE_PAGES = ['/', '/index.html', '/doggo.html']
tcpSocket = None
startedTime = None


def main():
    port = userInput()
    startServer(SERVER_ADDRESS, port)


# Takes user input, if user skips then port set to random
def userInput():
    print '>>> Enter the PORT number\n>>> Press ENTER to skip\n'
    userInput = raw_input()
    
    # Determine whether port is fixed or random 
    if (FIXED_PORT): port = 8080
    else: port = random.uniform(1025, 10000)

    if (userInput):
        # Only accept if port is higher than 1024
        if (int(userInput) > 1024): 
            port = userInput
            print 'Setting to: ' + str(port)
        else: 
            print 'Port number must be higher than 1024'
            sys.exit()
    # Set port value if skipped
    else: print '! SKIPPING: Setting PORT to ' + str(port) + '\n'

    return int(port)


# Starts the server on a given port and address
def startServer(serverAddress, serverPort):
    # Create server socket
    global tcpSocket
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.settimeout(TIMEOUT)

    # Bind the server socket to server address and server port, increment port until successful
    portBound = False
    while not portBound:
        try: 
            tcpSocket.bind((serverAddress, serverPort))
            tcpSocket.settimeout(100)
            portBound = True
        except:
            serverPort += 1
            print 'PORT ' + str(serverPort - 1) + ' is already in use, attempting to connect using PORT ' + str(serverPort)

    # Listen for connections to server socket
    tcpSocket.listen(MAX_CONNECTIONS)
    print 'Listening on ' + str(serverAddress) + ' | PORT: ' + str(serverPort) + '\n'
    global startedTime
    startedTime = time.time()

    # Keep server active
    serverActive = True
    while serverActive:
        # Close server if SIGINT
        signal.signal(signal.SIGINT, closeServer)

        # Accept new connections
        connectionSocket, address = tcpSocket.accept()

        # Handle request if connection is accepted
        if (connectionSocket):
            print 'Received a connection at: ' + str(address[0]) + ' | ' + str(address[1])
            handleRequest(connectionSocket)


# Handles the request that is made by the connecting client
def handleRequest(tcpSocket):
    # Receive request message from the client on connection socket
    tcpSocket.settimeout(TIMEOUT)
    data = tcpSocket.recv(2048).decode()
    data = data.split(' ')
    method, request = data[0], data[1]

    # Safety net to make sure user is using GET method
    if (method == 'GET'):	
        # Set default file to index.html
        if (request == '/'): request = '/index.html'
        if (request not in AVAILABLE_PAGES): request = '/404.html'
        print 'Client requested file ' + str(request) + ' from disk\n'
        
        # Read the corresponding file from disk
        try: 
            # Grab the file
            file = open(request[1:], 'r')
            requestedData = file.read().encode()
            file.close()

            # Pack the file into the header
            if (request == '/404.html'): 
                sendResponse(tcpSocket, (' ' + str(404) + ' Not Found'), requestedData)
            else: 
                sendResponse(tcpSocket, (' ' + str(200) + ' OK'), requestedData)

        except Exception as error:
            print error4


# Generates header according to the provided code
def createHeader(code):
    formattedTime = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
    header = 'HTTP/1.1 ' + code + '\n'
    header += 'Date: ' + formattedTime + '\n'
    header += 'Server: WebServer Example\n\n'
    return header.encode()


# Constructs the data to be sent and sends it to client
def sendResponse(tcpSocket, code, data):
    header = createHeader(code)
    data = header + str(data)
    tcpSocket.send(data)
    tcpSocket.close()


# Gently closes the server and provides useful info
def closeServer(signal, handler):
    tcpSocket.close()
    print 'Server Closed'
    ranFor = time.time() - startedTime
    print 'Server ran for: ' + '%.3f' % ranFor + ' seconds.'
    sys.exit()

# Execute main
if __name__ == "__main__":
    main()