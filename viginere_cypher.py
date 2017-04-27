#!/usr/bin/python

# A small python Script Viginere Cipher. Fun to program, learned interesting thing about lists of lists (see notes at end)
# Time ~ 5 hours (including googling/manual reading time)
# Works nicely, not too messy.
# Things to improve: File support, would need to deal with specials like \n and \r possibly.
#                   Again, smoother Argparse options and checks. Support for Windows (i'll learn some point...)
#                   Learn list comprehension to deal with awkward syntax better. Bughunt.
# RJM


import argparse
import sys
import string
import copy

# print the constructed viginere square
def print_square():
    for alpha in square:
        print " ".join(alpha)

# sort the lists of alphabets into correct order
def pop_it(times, alpha):
    count = 0
    while count < times:
        x=alpha.pop(0)
        alpha.append(x)
        count +=1

# build the list of lists of alphabets
def build_square():
    for i in range(26):
        square.append(copy.copy(alphabet))
    i=0
    for alpha in square:
        pop_it(i, alpha)
        i+=1
    return square

# expand the key to message length
def keygen(message, keyword):
    count=0
    keylist=list(keyword)
    while len(keylist) < len(message):
        keylist.append(keylist[count])
        count+=1
    return keylist

# encode the message
def encode(message, keylist):
    count=0
    encoded = ""
    for char in message:
        if char ==' ':
            encoded=encoded+' '
        else:
            key=ord(keylist[count])-97
            charval=ord(char)-97
            encoded = encoded + square[key][charval]
        count+=1
    return encoded

# decode a message with the keylist
def decode(encoded, keylist):
    decoded = ""
    count=0
    for char in encoded:
        if char == ' ':
            decoded=decoded+' '
        else:
            row= ord(keylist[count])-97
            column=square[row].index(char)
            decoded=decoded+square[0][column]
        count+=1
    return decoded

# argument parsing
parse=argparse.ArgumentParser(description="A small python script to encode or decode a message with a supplied key using a Viginere cipher",
                                epilog="If using -e or -d you must include both a -k KEY and -m MESSAGE. You can disply a Viginere Square without any other arguments")
parse.add_argument("-m", dest="Message", type=str, help="Message to Encode. Alpha characters and spaces only, enclose multiple words in quotes.")
parse.add_argument("-k", dest="Key", type=str, help="Cipher Key. Alpha characters only with no spaces.")
parse.add_argument("-d", dest="Decode", action="store_true", help="Decode -m (message). Must also include -k (Key)")
parse.add_argument("-e", dest="Encode", action="store_true", help="Encode -m (message). Must also include -k (Key)")
parse.add_argument("--display", dest="Display", action="store_true", help="Display Viginere Square. Not particularly useful but it looks nice!")
args=parse.parse_args()

# Argument checking

if len(sys.argv) < 2:
    print "No arguments supplied. Use -h or --help for more information"

if args.Display:
    print_square()

if (args.Encode or args.Decode) and not args.Key:
    print "Must include key!"
    sys.exit()
elif args.Key and not args.Message:
    print "Nothing to decode!"
    sys.exit()
elif args.Key and not (args.Encode or args.Decode):
    print "Please specify -e (encode) or -d (decode). Or even both!"

# square params
square=[]
alphabet = list(string.ascii_lowercase)
build_square()

# not sure why have to specify as string (argparse shd take care of that?)
# but do anyway, else no Type errors occur
keyword = str(args.Key)
message = str(args.Message)
keylist = keygen(message, keyword)

#format message + key. Add support for special chars later.
for char in message:
    if char.isalpha():
        char.lower()
    elif char == ' ':
        continue
    else:
        print "Message must be alpha only!"
        sys.exit()

for char in keyword:
    if char.isalpha():
        char.lower()
    else:
        print "Key must be alpha only! Do not use spaces"
        sys.exit()

# both encode and decode flags active. Mostly included for posterity but also for testing
if args.Encode and args.Decode:
    print "Encoding '%s' with key [%s]\n" %(message, keyword)
    encoded=encode(message, keylist)
    print encoded
    print "\n"
    print "Decoding '%s' with key [%s]\n" %(encoded, keyword)
    print decode(encoded, keylist)
    sys.exit()

if args.Encode:
    print "Encoding '%s' with key [%s]\n" %(message, keyword)
    print encode(message, keylist)
    sys.exit()
if args.Decode:
    print "Decoding '%s' with key [%s]" %(message, keyword)
    print decode(message, keylist)
    sys.exit()



# Some Notes.
# interesting problem with List of Lists - when adding 'alphabet' actually adds multiple copies of the SAME list.
# Altering one of these lists alters them all. Have to add copies of alphabet to square
# i.e square.append(alphabet) * 26 doesn't work. Remember this!
# (muchos thanks, Redditors! /r/learnpython)
#
#  making a slice of a list makes a new list, as does adding 2 lists together, so you could just do this
#  for i in range(26):
#     square.append(alphabet[i:] + alphabet[:i])
# copy not needed since the slice and add creates new lists.
