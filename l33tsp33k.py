#!/usr/bin/python
# reddit daily challenge - easy mode
# l33tspeak generator
import sys

if len(sys.argv) < 2:
    print "[USAGE] : ./l33tsp33k.py [string]"
    sys.exit()
string=sys.argv[1]

letters=['A', 'B', 'E', 'I', 'L', 'M', 'N', 'O', 'S', 'T', 'V', 'W']
leets=['4', '6', '3', '1', '1', '(V)', '(\)', '0', '5', '7', '\/', '`//']

string_out=""
for letter in string.upper():
    if letter in letters:
        index=letters.index(letter)
        string_out+=leets[index]
    else:
        string_out+=letter
print string_out
