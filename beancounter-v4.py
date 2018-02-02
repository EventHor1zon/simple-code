#!/usr/bin/python

# Beancounter v0.1
# python program to be run on the pi z w
# capture AP and MAC noise
# Parse info
# maybe even some cleartext sniffing
# maybe router types
# see where it goes

# Bean Bay Beans
# They're the Beaniest!

import sys
import subprocess
import os
import time
import gzip
import shutil

WLAN_DEV="wlp9s0"

# problem - opening file if it doesn't exist requires W only priveleges
# but closing then re-opening for read doesnt re-open the file
# problem with permissions maybe?


def mon():
    sep_string = "~~~~~~~~~~~~~~~~~~~~~~~"
    procF=open("process_file", "w")
    airmon=subprocess.Popen(["airmon-ng", "start", WLAN_DEV], stdout=procF)
    airmon.kill()
    procF.close()
    process_down=[]
    testfile=open("process_file", "r")
    print "Right about now I should be printing the process file..."
    for line in testfile.readlines():
        print line
    #    words=line.split()
    #    if len(words) > 0 and words[0].isdigit():
    #        process_down.append(words[0])
    procF.close()
    log_it("Mon enabled")
    print "Between processes"
    print process_down
    for element in process_down:
        try:
            print "killing :" + str(element)
            ERRBUFF=""
            kill=subprocess.Popen(["kill", element], stdout="/dev/null", stderr=ERRBUFF)
        except:
            errstring = "Non-Fatal Error: Error closing process: " + ERRBUFF
            log_it(errstring)
            print "Couldn't kill " + element
            continue
    return

def dump():
    timelog=time.strftime("%H%M", time.localtime())
    data_file = "Data_File"+timelog
    with open(data_file, "w+") as procF:
        dump=subprocess.Popen(["sudo", "airodump-ng", "--ignore-negative-one", "--output-format", "csv", "-a", "-w", "-", "mon0"], stdout=procF.fileno())
        log_it("Starting Capture")
        f_stat=os.stat("./process_file")
        while(f_stat.st_size < 104000000):
            time.sleep(5)
            f_stat=os.stat("./process_file")
        dump.kill()
        log_it("File full - Compressing")
        compress()
    return 1

def compress():
    try:
        with open("data_file", "rb") as f_in, gzip.open("air_chives.gzip", "wb") as f_out:
            try:
                shutil.copyfileobj(f_in, f_out)
            except shutil.Error:
                f_in.write("======================ERROR COMPRESSING=========================")
                errstring = "Err Code: " + str(shutil.Error.errno) + " - Err: " + shutil.Error.strerr + "Error Compressing"
                f_in.write(errstring)
                log_it(errstring)
    except:
        log_it("Error Opening compression files. Exiting")
        sys.exit(1)

def log_it(string):
    timenow = time.strftime("%H%M%S%a%b%d", time.localtime())
    with open("beancounter_log_file", "wr") as log:
        write_string=timenow + " : " + string + "^^^"
        log.write(write_string)



def main():

    mon()
    #dump()


if __name__ == '__main__':
	main()
