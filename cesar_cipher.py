#!/usr/bin/python


# ceasar cipher #
# start with fixed string, work up to importing file to encode/decode #
# decent program, pretty basic concepts, fun to write
# Could improve: Argparse usage, including proper includes/sanity checking
#               Needs searched for bugs
#               Upper chars nice but not neccesary, encoding symbols etc.
#               auto outFile naming convention



# Imports

import argparse
import sys
import string

# Cipher function #
# changes strings with cipher

def cipher(message, shift):
    encoded=""
    for char in message:
            if char.isspace():
                char=' '
            elif not char.isalnum():
                char=char
            elif char.isalnum():
                val = ord(char.lower())+shift
                if val < lower:
                    val = (upper+1) - (lower-val)
                if val > upper:
                    val = (lower-1) + (val-upper)
                char = chr(val)
            else:
                char=char
            encoded=encoded+char
    return encoded

# file handling function
# itterates over lines in a file and writes them to outFile

def file_crypt(in_f, out_f, shift):
    string=""
    try:
        inFile = open(in_f, "r")
        outFile = open(out_f, "w")
    except:
        raise
    print "Writing to %s" %outFile
    for line in inFile:
        string=cipher(line, shift)
        outFile.write(string)
    inFile.close()
    outFile.close()

# decrypt mode
# Iterates over all possibilities

def decipher(message):
    for i in range(26):
        phrase=cipher(message, i)
        print "[+] : " + phrase + ": shift %d" %i

# quick function to display an alphabet with applied shift val
# mostly for debugging, but also fun to include

def display(shift):
    alpha=list(string.ascii_lowercase)
    for letter in alpha:
        letter=letter+":"+cipher(letter, shift)
        print letter

# Parse arguments #

parse=argparse.ArgumentParser()
parse.add_argument("-s", dest="Shift", type=int, help="Cipher shift (+/-)", )
parse.add_argument("-f", dest="File", type=str, help="File to cipher (relative or absolute path)")
parse.add_argument("-l", dest="Line", type=str, help="Line to cipher. Enclose in quotes")
parse.add_argument("-o", dest="FileOut", type=str, help="File to write encoded file to")
parse.add_argument("-c", dest="Crack", action="store_true", help="Show all caesar translations of an included line(-l) (Used for unknown shift)")
parse.add_argument("--display", dest="Display", type=int, help="Display alphabet with supplied shift")
args=parse.parse_args()

# Usage info #
upper = 122
lower = 97
message=""
shift=0
test_message="testing all ze things!"

# Sanity Checks #
if args.Display:
    shift=args.Display
    display(shift)
    sys.exit()

if args.Shift == None:
    print "Shift not specified (default 0)"
else:
    shift=args.Shift

if args.File and args.Line:
    print "Please choose only one of File or Line"
    sys.exit()
elif args.File and not args.FileOut:
    print "No File Out specified"
    sys.exit()
elif args.File and args.FileOut:
    print ""
    infile = args.File
    outfile = args.FileOut
    file_crypt(infile, outfile, shift)
elif args.Line:
    message=args.Line
    if args.Crack:
        print "Deciphering : " + message
        decipher(message)
    else:
        print "Ciphering : " + message
        print cipher(message, shift)
else:
    print "Nothing to cipher! Please use either -l for line or -f for file"
    sys.exit()
