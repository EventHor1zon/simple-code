#!/usr/bin/python

'''
Simple ascii clock in python
Beginner Level. Programming challenge #145
    R.M
    additions: little hard to see. Could improve spacing between the numbers slightly.
                addition of flag for colour settings? Could do by modifying the strings in the slates       XXX DONE XXX
                using list comprehension? Adding terminal ascii colours? Green on red dots would look good. XXX DONE XXX
                make compatible on windows, good habit. Read sys and adjust clear-screen function.
                Adding a changeable format wouldn't be too hard i.e 12/24 hour clock
                graceful exit on ctl-c perhaps? Clean up argparse options/bug hunting
    appraisal: not bad for 3 hours, worked out some timesaving measures, even a little
                optimization. Some bits are a bit scrappy, could do with being tidied up or optimised

'''

#define slates: i.e ascii display numbers

slate1=[['.','.','X','.','.'],
        ['.','X','X','.','.'],
        ['.','.','X','.','.'],
        ['.','.','X','.','.'],
        ['.','.','X','.','.'],
        ['.','.','X','.','.'],
        ['.','.','X','.','.'],
        ['.','.','X','.','.']]
slate2=[['.','X','X','X','.'],
        ['X','.','.','.','X'],
        ['.','.','.','.','X'],
        ['.','.','.','.','X'],
        ['.','.','.','X','.'],
        ['.','.','X','.','.'],
        ['.','X','x','.','.'],
        ['X','X','X','X','X']]
slate3=[['.','X','X','X','.'],
        ['X','.','.','.','X'],
        ['.','.','.','.','X'],
        ['.','.','X','X','x'],
        ['.','.','.','.','X'],
        ['.','.','.','.','X'],
        ['X','.',',','.','X'],
        ['.','X','X','X','.']]
slate4=[['.','.','.','X','.'],
        ['.','.','X','X','.'],
        ['.','X','.','X','.'],
        ['X','.','.','X','.'],
        ['X','.','.','X','.'],
        ['X','X','X','X','X'],
        ['.','.','.','X','.'],
        ['.','.','.','X','.']]
slate5=[['X','X','X','X','X'],
        ['X','.','.','.','.'],
        ['X','.','.','.','.'],
        ['X','X','X','.','.'],
        ['.','.','.','X','.'],
        ['.','.','.','.','X'],
        ['X','.','.','.','X'],
        ['.','X','X','X','.']]
slate6=[['.','.','X','X','.'],
        ['.','X','.','.','.'],
        ['X','.','.','.','.'],
        ['X','.','.','.','.'],
        ['X','X','X','X','.'],
        ['X','.','.','.','X'],
        ['.','X','.','.','X'],
        ['.','.','X', 'X','.']]
slate7=[['X','X','X','X','X'],
        ['.','.','.','.','X'],
        ['.','.','.','X','.'],
        ['.','.','X','.','.'],
        ['.','.','X','.','.'],
        ['.','X','.','.','.'],
        ['.','X','.','.','.'],
        ['.','X','.','.','.']]
slate8=[['.','X','X','X','.'],
        ['X','.','.','.','X'],
        ['X','.','.','.','X'],
        ['.','X','X','X','.'],
        ['.','X','X','X','.'],
        ['X','.','.','.','X'],
        ['X','.','.','.','X'],
        ['.','X','X','X','.'],]
slate9=[['.','X','X','X','.'],
        ['X','.','.','.','X'],
        ['X','.','.','.','X'],
        ['.','X','X','X','X'],
        ['.','.','.','.','X'],
        ['.','.','.','X','.'],
        ['.','.','X','.','.'],
        ['.','X','.','.','.']]
slate0=[['.','X','X','X','.'],
        ['X','.','.','.','X'],
        ['X','.','.','.','X'],
        ['X','.','.','.','X'],
        ['X','.','.','.','X'],
        ['X','.','.','.','X'],
        ['X','.','.','.','X'],
        ['.','X','X','X','.']]
slateZ=[['.','.','.'],
        ['.','@','.'],
        ['.','@','.'],
        ['.','.','.'],
        ['.','.','.'],
        ['.','@','.'],
        ['.','@','.'],
        ['.','.','.']]

# empty strings to fill
timenow = ""
fg = ""
bg = ""

# functions used in program

def print_time(h1, h2, m1, m2):
    for i in range(8):
        print(" ".join(h1[i]) + " "
                + " ".join(h2[i]) + " "
                + "".join(slateZ[i]) + " "
                + " ".join(m1[i]) + " "
                + " ".join(m2[i]))

def print_slate(slate):
    for i in range(8):
        print(" ".join(slate[i]))

def set_colours(fg, bg):
    colour_slate(slate1, fg, bg)
    colour_slate(slate2, fg, bg)
    colour_slate(slate3, fg, bg)
    colour_slate(slate4, fg, bg)
    colour_slate(slate5, fg, bg)
    colour_slate(slate6, fg, bg)
    colour_slate(slate7, fg, bg)
    colour_slate(slate8, fg, bg)
    colour_slate(slate9, fg, bg)
    colour_slate(slate0, fg, bg)
    colour_slate(slateZ, fg, bg)

def colour_slate(slate, fg, bg):
    length = len(slate[0])
    for row in slate:
        for i in range(length):
            if row[i] == '.':
                row[i] = bg + row[i]
            elif row[i] == 'X':
                row[i] = fg + row[i]
            elif row[i] == '@':
                row[i] = fg + row[i]

def map_slate(x):

    if x == '1':
        return slate1
    elif x == '2':
        return slate2
    elif x == '3':
        return slate3
    elif x == '4':
        return slate4
    elif x == '5':
        return slate5
    elif x == '6':
        return slate6
    elif x == '7':
        return slate7
    elif x == '8':
        return slate8
    elif x == '9':
        return slate9
    else:
        return slate0

# define colour values

RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
MAGENTA = '\033[1;35m'
CYAN = '\033[1;36m'

# imports

import sys, argparse
from time import strftime, localtime, sleep

# handle colour arguments

opts = argparse.ArgumentParser(description="a simple ascii clock with colours!")
opts.add_argument("-f", dest="FG_colour", help="Colour of numbers on the ascii clock: \n r - red \n g - green \n y - yellow \n b - blue \n m - magenta \n c - cyan")
opts.add_argument("-b", dest="BG_colour", help="Colour of Background of ascii clock: \n r - red \n g - green \n y - yellow \n b - blue \n m - magenta \n c - cyan")
args = opts.parse_args()

if args.FG_colour:
    if args.FG_colour == 'r':
        fg = RED
    elif args.FG_colour == 'g':
        fg = GREEN
    elif args.FG_colour == 'y':
        fg = YELLOW
    elif args.FG_colour == 'b':
        fg = BLUE
    elif args.FG_colour == 'm':
        fg = MAGENTA
    elif args.FG_colour == 'c':
        fg = CYAN
    else:
        fg = fg
if args.BG_colour:
    if args.BG_colour == 'r':
        bg = RED
    elif args.BG_colour == 'g':
        bg = GREEN
    elif args.BG_colour == 'y':
        bg = YELLOW
    elif args.BG_colour == 'b':
        bg = BLUE
    elif args.BG_colour == 'm':
        bg = MAGENTA
    elif args.BG_colour == 'c':
        bg = CYAN
    else:
        bg = bg
if args.FG_colour or args.BG_colour:
    set_colours(fg, bg)

# main clock loop

while(1):
    if timenow != strftime("%H%M", localtime()):
        timenow = strftime("%H%M", localtime())
        hour1 = map_slate(timenow[0])
        hour2 = map_slate(timenow[1])
        minute1 = map_slate(timenow[2])
        minute2 = map_slate(timenow[3])
        print("\033c")
        print_time(hour1, hour2, minute1, minute2)
    sleep(1)
