#!/usr/bin/env python

import socket
import os

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#listening to connections " listen to any address i can listen o on this computer"
clientSocket.bind(("0.0.0.0", 8001))

# numebr being how many connections we want to listen to
clientSocket.listen(5)
# tellingserver tht it can uickly rese addr
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

while True:

	(incomingSocket, port) = clientSocket.accept()
	print "we got a connection from %s!" % (str(port))

	pid = os.fork()
	if (pid == 0): # we must e the chid (cloned) proces, so we ill hanle proxyig for this client

		googleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		googleSocket.connect(("www.google.com", 80))

		#setting bot servers to be non blocking, error instead o wating
		incomingSocket.setblocking(0)
		googleSocket.setblocking(0)

		while True:
			#this half of the loop forwards from client to google
			skip = False
			try:
				part = incomingSocket.recv(1024)
			except socket.error, exception:
				if exception.errno == 11:
					skip = True
				else:
					raise

			if not skip:

				if (len(part) > 0):
					print ">" + part
					googleSocket.sendall(part)
				else:
					# part will be empty when its done
					exit(0)

			#this half of the loop wll return google tothe client
			skip = False
			try:
				part = googleSocket.recv(1024)
			except socket.error, exception:
				if exception.errno == 11:
					skip = True
				else:
					raise

			if not skip:
				if (len(part) > 0):
					print "<" + part
					incomingSocket.sendall(part)
				else:
					# part will be empty when its done
					exit(0)
