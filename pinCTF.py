#!/usr/bin/python3

import os
import sys
import argparse
import IPython
import configparser
import string
from subprocess import PIPE, Popen


def main():
    #Defaults
    configLocation = "config.ini"
    config = checkConfig(configLocation)

    pinLocation = config.get("DEFAULTS","PinLocation")
    libraryLocation = config.get("DEFAULTS","LibraryLocation")
    count = config.get("DEFAULTS","Count")
    seed = config.get("DEFAULTS","Seed")
    variable_range = config.get("DEFAULTS","Range")

    #a-Z
#    variable_range = string.ascii_letters

    parser = argparse.ArgumentParser()

    #Add arguments
    parser.add_argument('-f','--file',help="file to run pin against")
    parser.add_argument('-a', '--arg',help="Trace instructions for passed in argument",action="store_true")
    parser.add_argument('-al', '--argLength',help="Trace instructions for passed in argument length",action="store_true")
    parser.add_argument('-i', '--input',help="Trace instructions for given input",action="store_true")
    parser.add_argument('-il', '--inputLength',help="Trace instructions for input length",action="store_true")
    parser.add_argument('-p', '--pinLocation',help="Location of pin's directory")
    parser.add_argument('-l', '--pinLibraryLocation',help="Location of pin's instruction0.so libraries")

    #If length based instruction counting you can provide a count
    parser.add_argument('-c','--count',help="MaxLength to for length based pin")

    #If arg or input based, we need a seed to start and can use a different
    #range to iterate over
    parser.add_argument('-s','--seed',help="Initial seed for input or arg pin")
    parser.add_argument('-r','--range',help="range of characters to iterate pin over")

    #Optionally we can specify a length for our seed
    parser.add_argument('-sl','--seedLength',help="Initial seed length for input or arg pin")

    #Parse Arguments
    args =parser.parse_args()

    #Check for argument errors
    if not args.file:
        print("[-] Error missing file")
        exit(0)
    if not (args.arg or args.argLength or args.input or args.inputLength): #TODO change to A xor B xor C xor D
        print("[-] Error missing pin instruction counting technique")
        exit(0)
    if args.pinLocation:
        pinLocation = args.pinLocation
    if args.pinLibraryLocation:
        libraryLocation = args.pinLibraryLocation
    if args.count:
        count = int(args.count)
    if args.seedLength:
        seed = 'A'*int(args.seedLength)
    if args.seed:
        seed = args.seed
    if args.range:
        variable_range = args.range

    #Can I get a switch statement please?
    if args.argLength:
        argLengthTuple = pinLength(pinLocation,libraryLocation,args.file,count,arg=True)
        print("[+] Found Length {} : Count {}".format(argLengthTuple[0], argLengthTuple[1]))

    if args.inputLength:
        inputLengthTuple = pinLength(pinLocation,libraryLocation,args.file,count,arg=False)
        print("[+] Found Num {} : Count {}".format(inputLengthTuple[0], inputLengthTuple[1]))

    if args.arg:
        pattern = pinIter(pinLocation,libraryLocation,args.file,seed,variable_range,arg=True)
        print("[+] Found pattern {}".format(pattern))

    if args.input:
        pattern = pinIter(pinLocation,libraryLocation,args.file,seed,variable_range,arg=False)
        print("[+] Found pattern {}".format(pattern))

#Checks for existence of config
#Creates config if not found, else returns config
def checkConfig(configPath):
    config = None
    if not os.path.isfile(configPath):

        print("[-] No config found. Building now")

        cwd = os.getcwd()

        config = configparser.ConfigParser()
        config.add_section("DEFAULTS")

        #Set defaults if no config is found
        config.set("DEFAULTS","PinLocation","")
        if os.path.isdir("{}/pin".format(cwd)):
            config.set("DEFAULTS","PinLocation","{}/pin".format(cwd))

        config.set("DEFAULTS","LibraryLocation","")
        if os.path.isdir("{}/obj-ia32".format(cwd)):
            config.set("DEFAULTS","LibraryLocation","{}/obj-ia32".format(cwd))

        config.set("DEFAULTS","Count","20")
        config.set("DEFAULTS","Seed","ABCD")
        config.set("DEFAULTS","Range","abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-")

        configFile = open(configPath,'w')
        config.write(configFile)
        configFile.close()
    else:
        config = configparser.ConfigParser()
        config.read(configPath)

    return config

def readCount():
    inscountFileName = "inscount.out"
    inscountFile = open(inscountFileName)
    line = inscountFile.read()
    count = int(line.split(' ')[1])
    inscountFile.close()
    return count

def sendPinArgCommand(pin,library,binary,arg):
    #The delay given by Popen causes inconsistencies in PIN
    #So use os.system instead
    COMMAND = "{}/pin -t {}/inscount0.so -- {} {} > /dev/null".format(pin,library,binary,arg)
    os.system(COMMAND)

    count = readCount()
    return count

def sendPinInputCommand(pin,library,binary,input):
    
    #The delay given by Popen causes inconsistencies in PIN
    #So use os.system instead
    ARGS = "{}/pin -t {}/inscount0.so -- {} ".format(pin,library,binary)

    #Send the output to /dev/null since it will pollute the screen otherwise
    os.system("echo {} | {} > /dev/null".format(input,ARGS))

    count = readCount()
    return count

def pinLength(pin,library,binary,length,arg=False):
    lengthDict = {}
    for i in range(1,int(length+1)):
        if arg:
            count = sendPinArgCommand(pin,library,binary,'A'*(i))
        else:
            count = sendPinInputCommand(pin,library, binary, 'A' * (i))
        sys.stdout.write("[~] Trying {}\r".format('A'*(i)))
        sys.stdout.flush()
        lengthDict[i] = count

    #Get largest count value
    largestCount = 0
    largestNum = 0
#    print("{:<4} : {:<15}".format("Num","Instr Count"))
    for num in lengthDict:
        if lengthDict[num] > largestCount:
            largestCount = lengthDict[num]
            largestNum = num
 #       print("{:<4} : {:<15}".format(num,lengthDict[num]))
    return (largestNum,largestCount)

def pinIter(pin,library,binary,seed,variable_range,arg=False):

    seedLength = len(seed)

    for i in range(seedLength):
        rangeDict = {}
        for item in variable_range:
            #Exchange value in seed for our range values
            #Python strings can't do it, so we use a list

            sys.stdout.write("[~] Trying {}\r".format(seed))
            sys.stdout.flush()

            seedList = list(seed)
            seedList[i] = item
            seed = ''.join(seedList)
            if arg:
                count = sendPinArgCommand(pin,library,binary,seed)
            else:
                count = sendPinInputCommand(pin,library,binary,seed)
            rangeDict[item] = count

        # Get largest count value
        largestCount = 0
        largestItem = 0
  #      print("{:<4} : {:<15}".format("Num","Instr Count"))
        #for num in rangeDict:
        for k, v in rangeDict.items():
            if v > largestCount:
                largestCount = v
                largestItem= k
 #           print("{:<4} : {:<15}".format(k,v))

        #Slot the value in
        seedList = list(seed)
        seedList[i] = largestItem
        seed = ''.join(seedList)
        print("[+] iter {} using {} for {}".format(i,largestItem,seed))
    return seed


main()
