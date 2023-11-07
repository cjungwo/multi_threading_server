import socket
import threading
import sys

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server open')

serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print("Started listening ...")


def ClientSocketHandler(clientSocket, addr):
    while True:
        try:
            message = clientSocket.recv(1024).decode()
            print(f"Get message : {message}") # GET /HelloWorld.html HTTP/1.1 ...
            filename = message.split()[1] # /HelloWorld.html
            f = open(filename[1:]) # HelloWorld.html
            outputdata = f.read()
            f.close()
            # Send one HTTP header line into socket
            # Fill in start
            successMessage = "HTTP/1.1 200 OK"
            clientSocket.send(successMessage.encode())
            clientSocket.send("\r\n".encode())
            print(f"Send connection success message to {addr[0]}")
            # Fill in end
            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                clientSocket.send(outputdata[i].encode())
            
            print(f"Send total {str(len(outputdata))} packets to {addr[0]}")
            clientSocket.send("\r\n".encode())

        except IOError:
            # Send response message for file not found
            # Fill in start
            errorMessage = "HTTP/1.1 404 Not Found"
            print(errorMessage)
            clientSocket.send(errorMessage.encode())
            clientSocket.send("\r\n".encode())
            # Fill in end

        finally:
            clientSocket.close()
            print(f"Closed Connection to client ({addr[0]} :{addr[1]})")
            break

while True:
    try:
        print("Ready to serve ...")
        clientSocket, addr = serverSocket.accept()
        print(f"Connect to client ({addr[0]} :{addr[1]})")
        # Start the new clientSocket thread
        threading._start_new_thread(ClientSocketHandler, (clientSocket, addr))
    except e:
        break
    

serverSocket.close()
sys.exit()