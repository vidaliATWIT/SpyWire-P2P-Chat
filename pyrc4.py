# -*- coding: utf-8 -*-
"""
Created on Sun May  2 14:17:36 2021

@author: vidali
"""

class rc4:
    S = []##S array
    T = []##Key array

    k = "5551sdfazxc5345234ss52345" ##key
    PT = "" ##plainText
    keyStream = ""
    
    def __init__(self, key):
        self.k=key
        ##self.PT=plainText
      
        for i in range(256): ##init S
            self.S.append(i)
        i=0
        for i in range(256): ##init T
            ii = i%len(self.k)
            appOut = "" ##appendOut
            if not (str.isnumeric(self.k[ii])): ##if number get the ascii value of the number
                tempStr = str(ord(self.k[ii]))
                appOut = tempStr
            else:
                appOut = self.k[ii] ##else just set the current character
            self.T.append(appOut)
        self.KSA()
        self.PSG()
                
    def KSA(self): ##Key Scheduling Algo
        j=0
        for i in range(256):
            j = (j + int(self.S[i]) + int(self.T[i])) % 256
            self.S[i], self.S[j] = self.Swap(self.S[i], self.S[j])
    
    def Swap(self, i, j):
        return j, i
    
    def PSG(self): ##Pseudo Random Generator
        j = 0

        for i in range(1, 256):
            j = (j + self.S[i])%256
            self.S[i], self.S[j] = self.Swap(self.S[i], self.S[j])
            t = (self.S[i] + self.S[j]) % 256
            ##print("KEYSTREAM: ", S[t])
            self.keyStream+=str(self.S[t])
            ##i+=1
            
    def uXOR(self, op1, op2):
        out = []
        for x in range(len(op1)):
            if type(op1[x]) is int:
                c1 = chr(op1[x])
            else:
                c1 = op1[x]
            c1 = ord(c1)
            c2 = int(op2[x])
            temp = c1 ^ c2
            out.append(temp)
        return out
    
    def mxor(self, message): ##encrypts/decrypts
        return self.uXOR(message, self.keyStream)

    def getString(self, op1):
        out = ""    
        for x in op1:
            out+=chr(x)
        return out
    def setKey(self, key):
        self.k = key
        
    def makeSendable(CS):
        outStream = ""
        for i in CS:
            outStream = outStream + chr(i)
        return outStream
    
    def setPT(self, plainText):
        self.PT = plainText