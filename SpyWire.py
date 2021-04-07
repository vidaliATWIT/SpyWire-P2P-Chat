# -*- coding: utf-8 -*-
"""
@author: vidali, waltersr
"""

import socket
import time
import random
from _thread import*

class Peer:
    inMessage="null"
    ThreadCount = 0
    onFlag = True
    client1Count = 0
    socketList = []
    printList = []
    socketBuffer = []
    userName = ''
    port = 9323 ##Change this number when testing locally via two separate consoles.

    ##initializes peer class
    def __init__(self):
      file = open("PeerList"+str(self.port)+".txt", "a")
      file.close()
      self.getPeersFromFile()
    
    ##main command line loop
    def mainLoop(self):
        socket=0
        start_new_thread(self.serverThread, (self,))
        time.sleep(.666)
        self.userName = input('Please input your username: ') ##type your name that will appear when chatting
        command = ''
        
        print("Input 'help' to see list of commands.")
        
        while (command!="exit"):
                try:
                    command = input("Input a command: " ) ##type a command
                    if (command=="message"): ##MESSAGE A PEER
                        peer = input("Which peer would you like to try?") 
                        if str.isnumeric(peer.split(":")[1]):
                            self.messagePeer((peer.split(":")[0], int(peer.split(":")[1])))
                    elif (command=="check"): ##CHECK PEER LIST CONNECTIONS
                        self.connectCheck()
                    elif (command=="see"): ##PRINT PEER LIST CONNECTIONS WHO ARE ONLINE
                        self.printPeerList()
                    elif (command=="send"): ##SHARE YOUR PEER LIST WITH ANOTHER PEER
                        peer = input("Which peer would you like to try?")
                        if str.isnumeric(peer.split(":")[1]):
                            self.sharePeers((peer.split(":")[0], int(peer.split(":")[1])))
                    elif (command=="add"): ##ADD ANOTHER PEER TO YOUR LIST
                        peer = input("Which peer would you like to add?")
                        self.addPeerToFile((peer.split(":")[0], int(peer.split(":")[1])))
                    elif (command=="help"): ##PRINT HELP COMMANDS
                        print("\nmessage = chat with a peer\ncheck = test connections with your peer list\nsee = print peers who are online\nsend = share your peer list with another peer\nadd = add a peer to your peer list\nexit = close the program")
                    elif (command=="exit"): ##EXIT THE PROGRAM
                        self.exitServer()
                except OSError as error: 
                    print("Peer was not online.")
                except IndexError as error:
                    print("Socket not properly initialized.")

                
    ##client method: message a peer
    def messagePeer(self, peer):
        serverName = peer[0]
        serverPort = peer[1]
        
        clientMessage = ""
        flag = True
        while (flag):
            clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            clientSocket.connect((serverName,serverPort))
            clientMessage = input("Input message: ")
            if(clientMessage=="--EXIT"):
                flag=False;
            else:
                clientMessage = self.userName + ": " + clientMessage
            clientSocket.send(clientMessage.encode())

            serverMessage = clientSocket.recv(1024).decode()
            print(serverMessage)
            clientSocket.close()
            
    ##client method: share peer socket list with another peer
    def sharePeers(self, peer):
        serverName = peer[0]
        serverPort = peer[1]
        sendStr = ""
        
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        
        clientSocket.send("--PEER".encode())
        time.sleep(3.0)

        for sock in self.socketList:
            ip = sock[0]
            port = sock[1]
            sendStr+= str(ip) + ":" + str(port) + "|"
        clientSocket.send(sendStr.encode())
        clientSocket.close()
     
    ##server method: receive, allocate, and add peer sockets to socket list
    def rcvPeerList(self, peerList):
        print("Reached here")
        peerArray = peerList.split("|")
        i=0
        for peer in peerArray:
            if (i<len(peerArray)-1):
                sock = peer.split(":")
                ##print(sock[0] + ":" + sock[1])
                self.addPeer(str(sock[0]), int(sock[1]))
                i+=1
                time.sleep(3)
     
    ##server thread: listening for connections
    def serverThread(self, nothing):
        serverMessage = ""
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverPort = self.port
        serverSocket.bind(('', serverPort))
        
        serverSocket.listen(5) 
        print('The server is ready to receive')
         
        flag = True
        
        while (flag):
            try:
                connectionSocket, addr = serverSocket.accept()
            except OSError as error:
                print("Could not connect!")
                break
            ##if Succeeded
            ##print ('Connected with ' + addr[0] + ';' + str(addr[1])) ##ip and port
            clientMessage = connectionSocket.recv(2048).decode() ##1024 is the bytes youll accept for a message
            if (clientMessage=="--PEER"):
                peerList = connectionSocket.recv(2048).decode()
                time.sleep(0.666)
                connectionSocket.close()
                self.rcvPeerList(peerList)
                ##print("DONE")

            elif (clientMessage=="--EXIT"):
                connectionSocket.close()
            elif (clientMessage=='--QUIT'):
                flag=False
            else:
                print(clientMessage)
                connectionSocket.send((clientMessage).encode())
        connectionSocket.close()
        serverSocket.close()
    
    ##server method: add a peer's socket to socket list
    def addPeer(self, serverName, portNumber):
        server = serverName
        port = int(portNumber)
        addFlag = True
        
        for sock in self.socketList:
            compStr1 = str(sock[0]) + ":" + str(sock[1])
            compStr2 = str(server) + ":" + str(port)
            if (compStr1 == compStr2 or port==self.port):
                addFlag=False
        if(addFlag):
            self.socketList.append((server, port))
            ##self.addPeerToFile((server, port)) ##saving shared peers to file
        else:
            print("Duplicate socket found! Not Copied.")
            
    ##client method: verify connections to sockets in socket list
    def connectCheck(self):
        self.printList.clear()
        for socketPair in self.socketList:
            testSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            
            try:
                testSocket.connect(socketPair)
                testSocket.send("--EXIT".encode())
            except socket.error as error: 
                print("Could not connect to " + str(socketPair[0]) +":" + str(socketPair[1]))
            else: 
                self.printList.append(str(socketPair[0]) +":" + str(socketPair[1]))
    
            testSocket.close()
            
    ##client method: print which peers are online        
    def printPeerList(self):
        for peer in self.printList:
            print(peer + " is online!")
            
    ##client method: exit the program
    def exitServer(self):
       clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       clientSocket.connect(('localhost',self.port))
       clientSocket.send("--QUIT".encode())
        
    ##client method: add peer socket to file
    def addPeerToFile(self, newPeer):
        duplicate = False
        self.getPeersFromFile()
        for socketPair in self.socketList:
            if socketPair[0] == newPeer[0] and socketPair[1] == newPeer[1]:
                duplicate = True
                print ("Duplicate socket detected. Not copied.")
        if not duplicate:
            socketListFile = open("PeerList"+str(self.port)+".txt", "a")
            socketListFile.write(str(newPeer[0]) + ":" + str(newPeer[1]) + "\n")
            self.socketList.append((str(newPeer[0]), int(newPeer[1])))
            socketListFile.close()
            
    ##client method: retreive peer list sockets from file
    def getPeersFromFile (self):
        duplicate = False
        socketListFile = open("PeerList"+str(self.port)+".txt", "r")
        socketPairs = socketListFile.readlines()
        for socketPair in socketPairs:
            duplicate = False
            for peer in self.socketList:
                if socketPair.split(":")[0] == peer[0] and int(socketPair.split(":")[1]) == peer[1]:
                    duplicate = True
            if not duplicate:
                self.socketList.append((socketPair.rsplit(":")[0],int(socketPair.split(":")[1])))
        socketListFile.close()
            
s = Peer() ##creates the Peer object
s.mainLoop() ##runs the main loop