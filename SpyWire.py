import socket
import threading
import pyrc4
import time
from _thread import*

from tkinter import *
from tkinter import font
from tkinter import messagebox
  
# GUI class for the chat
class GUI:
    
    rc4 =None
    key="2313sadklfjasdlfkjl"
    username = ""
    ip = ''
    port = 9091
    
    socketList = [""]
    
    peerList = {
        "":""
        }
    
    # constructor method
    def __init__(self):
        
        ## Peer List Files
        file = open("data/PeerList"+str(self.port)+".txt", "a")
        file = open("data/UsernameAssignment"+str(self.port)+".txt", "a")
        file.close()
        
        print(self.peerList[self.username])
        print(self.socketList[0])
        
        self.getPeersFromFile()
        
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw() 
        self.initLogin()
        self.Window.mainloop()

        
    def initReceiver(self):
        start_new_thread(self.serverThread, (self,))
        
    ##server thread: listening for connections
    def serverThread(self, nothing):
        serverMessage = ""
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.bind(('', self.port))
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
            clientMessage = connectionSocket.recv(2048).decode() 
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
            elif (clientMessage=="--GETNAME"):
                return(self.username)
            else:
                clientMessage = self.decrypt(clientMessage) ##decrypt message
                self.printToScreen(clientMessage)
                connectionSocket.send((clientMessage).encode())
        connectionSocket.close()
        serverSocket.close()
        
        
    def clearFrame(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
    def initSender(self):
        self.sender = Toplevel()
        self.sender.title(self.username)
        self.sender.resizable(width=False, height=False)
        self.sender.configure(width=400, height=300, bg="black")
        
        self.textCons = Text(self.sender,
                             width = 20, 
                             height = 2,
                             bg = "black",
                             fg = "white",
                             font = "Fixedsys 14", 
                             padx = 5,
                             pady = 5,
                             cursor="arrow",
                             relief=GROOVE)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.085)
      
        self.labelHead = Label(self.sender,
                             bg = "black", 
                              fg = "white",
                              text = self.username,
                               font = "Fixedsys 13 bold",
                               pady = 5,
                               relief=GROOVE)
          
        self.labelHead.place(relwidth = 1)
          
        self.labelBottom = Label(self.sender,
                                 bg = "black",
                                 fg = "white",
                                 height = 35,
                                 relief=GROOVE)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.75)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "black",
                              fg = "white",
                              font = "Fixedsys 13",
                              relief=GROOVE)
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.05,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
        
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Fixedsys 10 bold", 
                                width = 20,
                                bg = "black",
                                fg = "white",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.05, 
                             relwidth = 0.22)
        self.outPeer = StringVar()
        self.outPeer.set("Peer")
        self.peerMenu = OptionMenu(self.labelBottom, self.outPeer, *self.peerList.keys())
        self.peerMenu.config(bg='black', fg='white', font="Fixedsys 10")
        
        self.peerMenu.place(relx = 0.55,
                             rely = 0.070,
                             relheight = 0.05, 
                             relwidth = 0.44)
        
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
        
        # Add peer button
        self.addButton = Button(self.labelBottom,
                                text = "Add Peer",
                                font = "Fixedsys 10 bold", 
                                width = 20,
                                bg = "black",
                                fg = "white",
                                command = lambda : self.initAddPeer())
          
        self.addButton.place(relx = 0.011,
                             rely = 0.070,
                             relheight = 0.05, 
                             relwidth = 0.22)
        
          
        self.textCons.config(state = DISABLED)
        
    
    def initAddPeer(self):
        self.sender.withdraw()
        self.addPeerWin = Toplevel()
        self.addPeerWin.title("Add Peer")
        self.addPeerWin.resizable(width=False, height=False)
        self.addPeerWin.configure(width=400, height=150, bg="black")
        self.addPeerWin.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
        
        #set ip port label
        self.ip_port = Label(self.addPeerWin, text="ip:port:", justify=LEFT,
                             font="Fixedsys 12 bold", bg="black", fg='white')
        self.ip_port.place(relheight = .15, relx=.27, rely=.32, anchor="center")
        
        #set default username
        self.set_username = Label(self.addPeerWin, text="username:", justify=LEFT,
                             font="Fixedsys 12 bold", bg="black", fg='white')
        self.set_username.place(relheight = .15, relx=.27, rely=.57, anchor="center")
        
        ##input ip:port
        self.input_ip_port = Entry(self.addPeerWin, font="Fixedsys 10", bg="black", fg="white", relief=GROOVE)
        self.input_ip_port.place(relheight=.15, relx=.40, rely=.25)
        
        ##input username
        self.input_username = Entry(self.addPeerWin, font="Fixedsys 10", bg="black", fg="white", relief=GROOVE)
        self.input_username.place(relheight=.15, relx=.40, rely=.50)
        
        ##add button
        self.ok_add = Button(self.addPeerWin, font="Fixedsys 10", text="add", bg="black", fg="white", relief=GROOVE, command = lambda: self.addPeer(self.input_ip_port.get()))
        self.ok_add.place(relheight=.15, relwidth=.20, relx=.40, rely = .75)
        
        
    def initLogin(self):
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300, bg="black")
        # create a Label
        self.pls = Label(self.login, 
                       text = "Enter username:",
                       justify = CENTER, 
                       font = "Fixedsys 14 bold",
                       bg="black",
                       fg="white")
          
        self.pls.place(relheight = 0.15,
                       relx = 0.5, 
                       rely = 0.19, anchor=CENTER)
     
        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
                             font = "Fixedsys 12",
                             bg='black',
                             fg='white',
                             relief=GROOVE)
          
        self.entryName.place( 
                             relheight = 0.1,
                             relx = 0.5,
                             rely = 0.34,
                             anchor=CENTER)
    
        # set the focus of the curser
        self.entryName.focus()
          
        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "login", 
                         font = "Fixedsys 14 bold", 
                         bg='black',
                         fg='white',
                         relief=GROOVE,
                         command = lambda: self.authenticate(self.entryName.get()))
          
        self.go.place(relx = 0.4,
                      rely = 0.50)
        
    def authenticate(self, name):
        self.username=name
        self.genCustomKey()##generates custom key with login info
        self.login.destroy()
        self.initReceiver() 
        self.initSender() ##receiver window
        self.sender.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        ##self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        self.messagePeer()
        
        
    ##client method: message a peer
    def messagePeer(self):
        peer = str(self.peerList[self.outPeer.get()]) ##gets the port under this username
        if(peer==""):
            return
        serverName = peer.split(":")[0]
        serverPort = int(peer.split(":")[1])
        
        clientMessage = self.msg
        flag = True
        
        if (self.connectCheck((serverName, serverPort))):
            clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            clientSocket.connect((serverName,serverPort))
    
            if(clientMessage=="--EXIT"):
                flag=False;
            else:
                self.printToScreen("To " + peer + ": " + clientMessage)
                clientMessage = self.username + ": " + clientMessage
                clientMessage = self.encrypt(clientMessage)
                ##clientMessage = self.mod(clientMessage) ##encrypts message
            clientSocket.send(clientMessage.encode())
    
            serverMessage = clientSocket.recv(1024).decode()
            print(serverMessage)
            clientSocket.close()
        
    def printToScreen(self, msg):
        self.textCons.config(state = NORMAL)
        self.textCons.insert(END,
                             msg+"\n")
                      
        self.textCons.config(state = DISABLED)
        self.textCons.see(END)
        
  
    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                  
                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.printToScreen(message)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                client.close()
                break 
          
    # function to send messages 
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))    
            break    
    # function to close window
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.Window.destroy()
    
    def encrypt(self, msg): ##generate a new encryptor with custom key returns msg + key
        cryptoid = pyrc4.rc4(self.key)
        msg = cryptoid.getString(cryptoid.mxor(msg))
        return msg + "?3x?" + self.key
        ##return msg + "?3x?" + cryptoid.keyStream
    def decrypt(self, msg): ##generates a new encryptor with custom key returns de-encrypted text
        grp = msg.split("?3x?")
        cryptoid = pyrc4.rc4(grp[1])
        msg = cryptoid.getString(cryptoid.mxor(grp[0]))
        return msg
    
    def genCustomKey(self):
        i=0
        a = self.key
        b = self.username
        c = self.key + self.username
        
        ##memory intensive        
        ##if (len(b)==0):
          ##  b="Unnamed Stranger"
        ##while(i<len(a)):
          ##  c = c + (chr(ord(a[i]) ^ ord(b[i%len(b)])))
            ##i+=1

        self.key= str(c)
        
    def addPeer(self, newPeer):
        try:
            peer = newPeer.split(":")
            ip, port = str(peer[0]), int(peer[1])
            self.addPeerToFile(newPeer)
            self.refreshPeerList()
        except:
            print("Peer format incorred. Nothing added...")
        self.addPeerWin.destroy()
        time.sleep(.3)
        self.sender.deiconify()
        
    ##client method: add peer socket to file
    def addPeerToFile(self, newPeer):
        duplicate = False
        self.getPeersFromFile()
        for socketPair in self.socketList:
            if (socketPair == newPeer):
                duplicate = True
                print ("Duplicate socket detected. Not copied.")
        if not duplicate:
            socketListFile = open("data/PeerList"+str(self.port)+".txt", "a")
            socketListFile.write(newPeer + "\n")
            usernameFile = open("data/UsernameAssignment"+str(self.port)+".txt", "a")
            usernameFile.write(newPeer+"///"+self.input_username.get() + "\n")
            self.socketList.append(newPeer)
            socketListFile.close()
            
    ##client method: retreive peer list sockets from file
    def getPeersFromFile (self):
        duplicate = False
        socketListFile = open("data/PeerList"+str(self.port)+".txt", "r")

        socketPairs = socketListFile.readlines()
        for socketPair in socketPairs:
            socketPair = socketPair.strip()
            duplicate = False
            for peer in self.socketList:
                peer = peer.strip()
                if (socketPair == peer):
                    duplicate = True
            if not duplicate:
                self.socketList.append(socketPair)
        socketListFile.close()
        self.getUsernameFromFile()
        
    ##client method: find username for ip and allocate
    def getUsernameFromFile(self):
        usernameFile = open("data/UsernameAssignment"+str(self.port)+".txt", "r")
        usernames = usernameFile.readlines()
        for username in usernames:
            username = username.strip()
            socket, username = username.split("///")
            self.peerList[username] = socket
        usernameFile.close()
        
    
    def connectCheck(self, socketPair):
        testSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            testSocket.connect(socketPair)
            testSocket.send("--EXIT".encode())
            return True
        except socket.error as error: 
            print("Could not connect to " + str(socketPair[0]) +":" + str(socketPair[1]))
            return False
        
    def refreshPeerList(self):
        self.outPeer = StringVar()
        self.outPeer.set("Peer")
        self.getUsernameFromFile()
        self.peerMenu = OptionMenu(self.labelBottom, self.outPeer, *self.peerList.keys())
        self.peerMenu.config(bg='black', fg='white', font="Fixedsys 10")
        self.peerMenu.place(relx = 0.55,
                             rely = 0.070,
                             relheight = 0.05, 
                             relwidth = 0.44)

# create a GUI class object
g = GUI()