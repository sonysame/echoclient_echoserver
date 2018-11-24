from socket import *
import sys

host=""
port=""


host=sys.argv[1]
port=sys.argv[2]

serverName=host

try:
	serverPort=int(port)

except:
	print("PORT should be decimal number! ERROR!")



try:
	
	clientSocket=socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName,serverPort))
	option=clientSocket.recv(1024)
	if(option=="on"):
		while True:
			message=raw_input("Input: ")
			clientSocket.send(message)
			while True:
				data=clientSocket.recv(1024)
				print(data)
	

	else:
		while True:
			message=raw_input("Input: ")
			clientSocket.send(message)
			data=clientSocket.recv(1024)
			print(data)
			if(data=="exit"):
				clientSocket.close()
				print("------------------------------------------------\n")
				break
	

	
	

except:
	clientSocket.close()
	print("error")

