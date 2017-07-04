#!/usr/bin/env python

# IRC connection uses a series of space separated 'forms' almost
# Ping - Pong sends bk and forth a string
# remember spaces and

import socket
import sys

class IRC:

    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, chan, msg):
        self.irc.send("PRIVMSG" + chan + " " + msg + "\n")

    def connect(self, server, channel, nickname):
        print "Connecting to: " + server
        self.irc.connect((server, 6667))
        self.irc.send("USER " + nickname + " " + nickname + " " + nickname + " " + nickname + " \n" )
        self.irc.send("NICK " + nickname + "\n")
        self.irc.send("JOIN " + channel + "\n")

    def get_text(self):
        text=self.irc.recv(2040)

        if text.find('PING') != -1:
            self.irc.send('PONG ' + text.split() [1] + "\r\n")
        return text
