from socket import *
import os
import webbrowser

chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
wholeFile = ""

serverName = input('Enter server host ip address : ') # 192.168.x.x
serverPort = int(input('Enter server port number : ')) # 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

fileName = input('Enter file name : ')
sendMessage = f"Get /{fileName} HTTP/1.1 \n Host: {serverName}:{serverPort}"

clientSocket.send(sendMessage.encode())

while True:
    modifiedSentence = clientSocket.recv(1024).decode()
    if modifiedSentence == "":
        break
    wholeFile += str(modifiedSentence)
    
print(wholeFile)
receivedFileName = "test.html"
status = int(wholeFile.split('\n')[0].split(' ')[1])
f = open(receivedFileName, "w")
if (status == 200):
    fileList = wholeFile.split()[3:]
    joinToFile = " ".join(fileList)
    f.write(joinToFile)
elif (status == 404):
    f.write(wholeFile)
f.close()
webbrowser.get(chrome_path).open('file://' + os.path.realpath(receivedFileName))

clientSocket.close()

print("TCP client completed - exiting")
