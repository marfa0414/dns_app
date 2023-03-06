
import json
from socket import *

serverPort = 53533
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('0.0.0.0',serverPort))
while True:
    message,clientAddress = serverSocket.recvfrom(2048)

    message = message.decode()

    message = json.loads(message)

    if len(message) ==2 :
        print(1)
        with open('address.json') as f:
            myMap = json.load(f)
        print(myMap)
        message = myMap[message["Name"]]
        message = json.dumps(message)
        serverSocket.sendto(message.encode(),clientAddress)
    elif len(message) ==4 :
        print(2)
        myfile = open("address.json","w")
        newDict = {
            message["Name"] : message
        }
        message = json.dumps(newDict)
        myfile.write(message)
        myfile.close()
        serverSocket.sendto(str(201).encode(),clientAddress)
