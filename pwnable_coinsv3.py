#!/usr/bin/python
# program to solve pwnable's coins challenge
# connect to server, get NUM of coins
# choose any number of coins to weigh
# One coin weighs 9, all others weigh 10
# find number of coin which weighs 9
# send to server
# repeat x100
# in under 10s
#===================================================
# code is disorganised and 
# heavily dependent on exact output of the server
# Interesting challenge though
#==================================================
# Had to upload to server and run locally as
# the connection speed was not fast enough to 
# find solution from external connection

def getArgs(buff):
        if "N=" in buff:
            if "Correct" in buff:
                buff_list=buff.split("\n")
                buff=buff_list[1]
            line=buff.split(" ")
            N=int(line[0].strip("N="))
            C=int(line[1].strip("C="))
        else:
            print "[-] Arguments not found"
            sys.exit()
        numlist=[]
        for i in range(N):
            numlist.append(i)
        return (numlist, C)

def solve(numlist, chances):
    if(len(numlist) > 1):
        sendlist=[]
        for i in range(len(numlist)/2):
            sendlist.append(numlist[i])
        sendline=' '.join(str(x) for x in sendlist) + "\n"
        sock.send(sendline)
        weight = sock.recv(16)
        if int(weight) % 10 != 0:
            solve(sendlist, chances-1)
        else:
            numlist2=numlist[len(sendlist):]
            solve(numlist2, chances-1)
    while chances > 0:
        sock.send(str(numlist[0]) + "\n")
        solve(numlist, chances-1)
    sock.send(str(numlist[0]) + "\n")
    print sock.recv(32)
    while True:
        print read_sock(sock)

def read_sock(sock):
    buff=""
    while True:
        buff+=sock.recv(2048)
        if "N=" in buff:
            print buff
            Args = getArgs(buff)
            solve(Args[0], Args[1])
    return buff


import sys
import socket

addr=socket.gethostbyname("www.pwnable.kr")
port=9007
conn=(addr, port)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print "[-] Failed to open socket. Error code: " + str(msg[0]) + " Error: " + msg[1]
    sys.exit()

try:
    sock.connect(conn)
except socket.error, msg:
    print "[-] Failed to connect. Error code: " + str(msg[0]) + " Error: " + msg[1]
    sys.exit()

#Intro Slide
print sock.recv(2048)

read_sock(sock)
print serial.recv(300)
