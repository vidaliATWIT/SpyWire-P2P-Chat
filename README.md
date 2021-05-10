===SPYWIRE P2P Chat Application===
Designed and programmed by Ian Vidal #vidali@wit.edu
Additional methods developed by Richard Waltters #waltersr@wit.edu
Current version: 0.2

==Description==

Spywire is a small p2p chat application that allows end-users to communicate directly. It allows any two users to chat so long as they are both online and know each other's public ip address as well as the configured static IP, in the default case 9091. 

==Running the program==

As of 5/10/2021 the application can now be compiled and used with its accompaniying GUI. Once done the program itself will ask for a display username and allow you to add a peer to your list and start chatting.

==Notes==

As of 5/10/2021 the command line version of the program is deprecated with develepment now focusing solely on the GUI counterpart. The original command line version is still available in this repo for archival purposes but will be removed once the program goes live with version 1.0 in the coming months. 

Requires socket and tkinter libraries to be installed in order to compile.

==New Additions version 0.2==
-total refactoring of the code to accomodate a custom gui.
-encryption is handled slightly differently to provide a more secure experience.
-removed the ability to share your entire peerlist with another peer. may be added back in the future.
-when adding a peer you may now specify a name by which to message them instead of using their ip:port.

==New Additions version 0.1==
-basic rc4 encryption module added..
-several utility methods related to encryption, decryption and sending added to main file.



==Commands [DEPRECATED]==

message = chat with a peer 
check = test connections with your peer list
see = print peers who are online
send = share your peer list with another peer
add = add a peer to your peer list
exit = close the program
--EXIT = exits the message line