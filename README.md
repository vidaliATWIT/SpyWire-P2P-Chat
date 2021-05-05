===SPYWIRE P2P Chat Application===
Designed and programmed by Ian Vidal #vidali@wit.edu
Additional methods developed by Richard Waltters #waltersr@wit.edu
Current version: 0.1

==Description==

Spywire is a small p2p chat application that allows end-users to communicate via command line. It allows any two users to chat so long as they are both online and know each other's public ip address as well as the configured static IP, in the default case 9323. 

==Running the program==

Currently the application can only be run by compiling the .py file and running it from the command line. Once done the program itself will ask for a display username and allow you to begin executing commands until the program is closed.

==Commands==

message = chat with a peer 
check = test connections with your peer list
see = print peers who are online
send = share your peer list with another peer
add = add a peer to your peer list
exit = close the program
--EXIT = exits the message line

Requires socket library to be installed in order to compile.

==New Additions version 0.1==
-basic rc4 encryption module added..
-several utility methods related to encryption, decryption and sending added to main file.
