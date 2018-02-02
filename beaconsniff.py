#!/usr/bin/python

# a basic packet sniffer using scapy library. Makes working with packets pleasant. Not unlike Planet Express #
# can sniff on regular or monitor mode but must be enabled first. Added some simple translation functions    #
# which could be useful elsewhere

# TODO: Add a more robust interface checking, perhaps a better library for it
# could use cack-handed sys/subprocess checks
# add proper argument checking and options
# fix keyboard interrupt try except things.

# SCAPY TIPS! To investigate layers in a field use IP().field_desc or use
# Pydoc scapy.layers.inet.IP etc to investigate packets and methods
# Also use ls(pkt) to view packet fields, contents & defaults
# Also use lsc() to show shit loads of scapy methods?
#
# used above methods to find the name section (possibly) in the dot11 headers



import sys
from scapy.all import *
iface = ''

# flags for use
DATA_FL = False
SNIFFPT_FL = False

requests=[]
wordlist = ["pass", "password", "username", "user", "usr", "id", "login", "admin", "administrator"]



def IPTypes(type):
    if type == 1:
        return "<ICMP>"
    elif type == 6:
        return "<TCP>"
    elif type == 17:
        return "<UDP>"
    elif type == 88:
        return "<IGMP>"
    else:
        return "<OTHER> Type: " + str(type)


def EtherTypes(type):
    # returns an easy to read string for common ethernet packet types #
    # if lots of 'others' appear can add more catagories later        #
    if hex(type) == "0x800":
        return "<IP4 Frame>"
    elif hex(type) == "0x806":
        return "<ARP FRAME>"
    elif hex(type) == "0x8808":
        return "<FLOW CONTROL>"
    elif hex(type) == "0x88CC":
        return "<LINK-LAYER FRAME>"
    else:
        return "<OTHER> " + str(hex(type))


def flagStringfromVal(val):
    # takes a value converts to string flag values
    # Unskilled Attackers Pester Real Security Folks
    # 32        16        8      4     2       1
    # Urgent Acknowledge Push Reset Synchronise Finish
    if val > 64:
        print "possible TCP flag error: val=" + str(val)
    flags = ""
    if val >= 32:
        val -= 32
        flags += "[URG] "
    if val  >= 16:
        val -= 16
        flags += "[ACK] "
    if val >= 8:
        val -= 8
        flags +="[PSH] "
    if val >= 4:
        val -= 4
        flags +="[RST] "
    if val >= 2:
        val -= 2
        flags +="[SYN] "
    if val >= 1:
        val-=1
        flags +="[FIN] "
    if val > 0:
        print "Possible TCP value error: val (postflags)=" + str(val)
    return flags


def tryInterface(iface):
    # tries an interface assignment.
    try:
        select([iface],[],[], timeout=3)
    except:
        print "Could not connect to " + iface + " - Please check your interface settings"
        sys.exit(1)

#def localRads(p):               # could maybe use filter here for easier... err.. Filtering. #
#    if p.haslayer(RadioTap)

def sniffTraffic(pkt):
    # sniff some basic internet traffic, print info about addresses and types #
    if pkt.haslayer(Ether): # Ether Src, Dst + Type [+ type name] #
        print "[2] #ETH# " + str(pkt[Ether].src) + " -> " + str(pkt[Ether].dst) + " Type: " + EtherTypes(pkt[Ether].type)
        if pkt.haslayer(IP): # IP src, dst,
            print "[3] #IP# " + str(pkt[IP].src) + " -> " + str(pkt[IP].dst) + " PROTO: " + IPTypes(pkt[IP].proto)
            if pkt.haslayer(TCP):
                print "[4] #TCP# Port " + str(pkt[TCP].sport) + " -> Port " + str(pkt[TCP].dport) + " ~FLAGS~ < " + flagStringfromVal(pkt[TCP].flags) + " >"
                print ""
            elif pkt.haslayer(UDP):
                print "[4] #UDP# Port " + str(pkt[UDP].sport) + " -> Port " + str(pkt[UDP].dport)

    # If print data flag... print data portion. Prints "." for outside char range
    if DATA_FL and pkt.haslayer(Raw) and len(pkt[Raw]) > 0:                         # prints packet data in lines
        data=str(pkt[Raw])                   # 8 bits long
        print "\t\n"
        for x in range(len(data)):
            if x % 8 == 0:
                print "\t\n"
            if ord(data[x]) > 31 and ord(data[x]) < 127:     # if char outside ascii range
                print data[x],
            else:
                print ".",
    if SNIFFPT_FL:
        sniffPT(str(pkt[Raw]));
    print "\n"


def sniffPT(data):
    # sniffs packet data for ascii chars, builds string then searches for small
    # list of strings. If it finds a keyword prints whole data.
    plainT=""
    for x in range(len(data)):
        if ord(data[x]) > 31 and ord(data[x]) < 127:     # if char inside ascii range
            plainT+=data[x]
    plainT.lower()
    if any(word in plainT for word in wordlist):
        print "\n[+] Found Keyword: { " + word + " }"
        print data




def sniffProbe(p):
    # sniffs RadioTap probes for 802.11 Probe request layers        #
    # if found then print the beacon request and the mac requesting #
    # upgrade to add the device name requesting. Chk WS for packets #

    if p.haslayer(Dot11ProbeReq):
        netProbe = p.getlayer(Dot11ProbeReq).info
        if netProbe not in requests:
            requests.append(netProbe)
            print "[+] Got request for beacon [" + netProbe + "] from " + str(p[Dot11].addr2) + " [" + p[Dot11].info + "]"
    print "\n"

def handleError(err):
    if err == "KeyboardInterrupt":
        print "Keyboard interrupt detected, exiting..."
        sys.exit(0)
    elif err == "EnvironmentError":
        print "Ah Ah Ah! You Didn't say the magic word!"
        sys.exit(1)
    # just some controlled error handling here. It currently doesn't fucking work. #


def main():
    usage = "USAGE: " + sys.argv[0] + " monitor|traffic"
    # usage allows for sniffing on established wifi or monitor mode card #
    # monitor mode scans for other beacon requests                       #
    # traffic mode scans some packets and displays details               #
    if len(sys.argv) < 2:                                       # need a mode
        print usage
        sys.exit(0)

    if sys.argv[1] == "monitor":                                 # monitor, sniff on mon0
        IF="mon0"                                                # interface var
        #tryInterface(iface)                                     # scapy function to try iface
        print "[+] Beginning Sniffing on " + IF + "...\n\n"      # verbosity!
        try:                                                     # in case of no mon0 interface...
            sniff(iface=IF, prn=sniffProbe, store = 0)           # begin sniff, callback to sniffProbe
        except KeyboardInterrupt:                                # ctrl-C quit
            raise
            print "KeyboardInterrupt detected, quitting..."
            sys.exit(0)
        except OSError: # exit
            raise

    elif sys.argv[1] == "traffic":                              # Traffic mode (tcpdump-esque)
        IF="wlp9s0"                                             # iface = wireless
        print "[+] Beginning Sniffing on " + IF                 # more verbs
        try:                                                    # try for easy exit
            sniff(iface=IF, prn=sniffTraffic, store = 0)        # sniff, callback sniffTraffic
        except KeyboardInterrupt:                                # ctrl-C quit
            print "Keyboard Interrupt detected, quitting..."
            sys.exit(0)
        except socket.error, msg:                               # check for sudo/other socket errors
            if str(msg[0]) == "1":                              # if no permission
                print "Ah Ah Ah! You Didn't say the magic word!\n(use sudo)"
            else:
                print "Error: "+msg[0] + " - " + msg[1]
            sys.exit(1)
    elif sys.argv[1] == "hybrid":
        IF="mon0"
        print("Begin sniffing on " + IF + " for local packets")
        try:                                                    # try for easy exit
            sniff(iface=IF, prn=localRads, store = 0)        # sniff, callback sniffTraffic
        except KeyboardInterrupt:                                # ctrl-C quit
            print "Keyboard Interrupt detected, quitting..."
            sys.exit(0)
        except socket.error, msg:                               # check for sudo/other socket errors
            if str(msg[0]) == "1":                              # if no permission
                print "Ah Ah Ah! You Didn't say the magic word!\n(use sudo)"
            else:
                print "Error: "+msg[0] + " - " + msg[1]
            sys.exit(1)

    else:                                                       # No args/bad spelling
        print usage                                             # usage
        sys.exit(0)                                             # exit


if __name__ == "__main__":
    main()
