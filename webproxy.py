#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys

# These following libraries do not help with the core function of the task
# these were checked with the professor and were said to be ok for use
import random # Used to generate random port number
import time # Used to get current time for the HTTP header
import signal # Used to detect CTRL-C
import os # Used to create a file directory for caching


MAX_CONNECTIONS = 4		# Max number of refused connections
FIXED_PORT = True		# Always attempt to use PORT 8080 if available
TIMEOUT = 100			# Socket blocking value
RECEIVE_SIZE = 2048     # Max size for the recv method
SERVER_ADDRESS = '127.0.0.1'
AVAILABLE_PAGES = ['/', '/index.html', '/doggo.html']
EXTENSIONS = ['.htm', '.ic', '.gi', '.js', '.css']
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
            tcpSocket.settimeout(TIMEOUT)
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
def handleRequest(sock):
    # Receive request message from the client on connection socket
    sock.settimeout(TIMEOUT)
    data = sock.recv(RECEIVE_SIZE).decode()
    
    # Extract host name and request from the GET
    if ('GET' in data):
        host = data.split()[1]
        if ('http://' in host): host = host.split('http://')[1]
        if ('/' in host): host, request = host.split('/', 1)
        else: request = ''
        request = '/' + request
        print '\nClient requesting ' + request + ' from ' + host
        
        # Check if request has already been cached locally
        cached = getCached(host, request)
        target = ''
        if (cached == False):
            print 'Cache not available, requesting new data'
            target = startProxy(data, host, request)
            handleCaching(host, request, target)
        else:
            print 'Cache is available, using data from disk'
            target = cached
        
        # Sends data to client that satisfies request
        sock.send(target)
        sock.close()
        print 'Data has been sent to client, closing request'
    else: sock.close()


# Fetches data from target and passes it back to client
def startProxy(data, host, request):
    # Create new socket
    proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxySocket.settimeout(TIMEOUT)

    # Connect and send request to target
    try:
        proxySocket.connect((host, 80))
        proxySocket.send(data)
    except Exception as error:
        print error

    # Wait until data is received, return with the data
    target = None
    while True:
        try: 
            target  = proxySocket.recv(RECEIVE_SIZE)
            if (target):
                proxySocket.close()
                break
        except: break
    
    return target


# Attempts to access cached webpage, returns false if it doesn't exist
def getCached(folder, file):
    # Define the file path
    if (file == '/'): file = '/index.html'
    if ('.' not in file): file += '.html'
    path = 'cached/' + folder + file
    
    # Attempt to open the file
    print 'Checking if page is cached at: ' + path
    try:
        file = open(path, 'r')
        target = file.read()
        file.close()
        return target
    except: return False


# Caches provided web page to local storage
def handleCaching(folder, file, data):
    # Define the file path
    if (file == '/'): file = '/index.html'
    if (file[-1:] == '/'): file = file[:-1]
    print file
    if ('.' not in file): file += '.html'
    print 'Caching ' + file + ' at: ' + './cached/' + folder + file

    # Creates new directory for the website
    directory = os.path.dirname('./cached/' + folder + '/')
    try:
        os.makedirs(directory)
    except: pass
    
    # Attempts to write the data into the file
    try:
        print directory[2:] + file
        f = open(directory[2:] + file, 'w+')
        target = f.write(data)
        f.close()
        return target
    except Exception as e:
        print e


# Gently closes the server and provides useful info
def closeServer(signal, handler):
    tcpSocket.close()
    print 'Server Closed'
    ranFor = time.time() - startedTime
    print 'Server ran for: ' + '%.3f' % ranFor + ' seconds.'
    sys.exit()


if __name__ == "__main__":
    main()