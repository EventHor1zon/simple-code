#!/usr/bin/python

# plan:
#
#   use socket to connect to an irc port
#   use irc functions to interact with irc bot
#   send command
#   read reply
#   slice the numbers out
#   do the maths
#   send the reply
#   print the flag
#
# Small program for solving root-me's IRC challenge. 
# Connect to IRC, PRIV_MSG bot, get numbers
# find answer and return it.
# Get tasty flag


from time import sleep
import os
import random
from my_irc import *
from math import sqrt

def main():
    channel = '#root-me_challenge'
    server = "irc.root-me.org"
    nickname = "bill_the_bot"
    USER='Candy'

    irc = IRC()
    irc.connect(server, channel, nickname)
    sleep(10)

    irc.send(USER, "!ep1")

    while 1:
        text = irc.get_text()
        print text
        if "PRIVMSG" in text and nickname in text:
            reply=text
            print reply
            mylist= reply.split(":")
            print mylist
            myinputs=str(mylist[2]).split("/")
            myinputs[1]=myinputs[1].strip("\r\n")
            print myinputs
            myanswer=sqrt(float(myinputs[0]))*float(myinputs[1])
            print myanswer
            mystring="!ep1 -rep " + str("%.2f" % myanswer)
            print mystring
            irc.send(USER, mystring)

# ok so full of debugs and def not able to extend to any other task. But IDIDIT!
# Coming soon, more IRC bots. Better IRC bots. German IRC bots. Maybe.

if __name__ == '__main__':
    main()
