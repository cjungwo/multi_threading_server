# import socket module
from socket import *
import sys  # In order to terminate the program

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
# Fill in start
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("Server Open")
# Fill in end

while True:
    # Establish the connection
    print("Server is ready ...")
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        print("Get message")
        filename = message.split()[1]
        f = open(filename[1:])
        print("Open file")
        outputdata = f.read()
        print("Read file")
        # Send one HTTP header line into socket
        # Fill in start
        successMessage = "HTTP/1.1 200 OK"
        connectionSocket.send(successMessage.encode())
        connectionSocket.send("\r\n".encode())
        print("Send connection success message")
        # Fill in end
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            print("Send packet " + str(i))

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
        break

    except IOError:
        # Send response message for file not found
        # Fill in start
        errorMessage = "404 Not Found"
        print(errorMessage)
        connectionSocket.send(errorMessage.encode())
        connectionSocket.send("\r\n".encode())
        # Fill in end

        # Close client socket
        # Fill in start
        connectionSocket.close()
        break
        # Fill in end
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding dat