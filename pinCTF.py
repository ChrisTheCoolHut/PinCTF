import os
import argparse
import IPython



def main():
    #Defaults
    pinLocation = "/home/chris/pin/pin-3.5-97503-gac534ca30-gcc-linux"
    libraryLocation = "/home/chris/pin/pin-3.5-97503-gac534ca30-gcc-linux/source/tools/ManualExamples/obj-ia32"
    count = 20
    seed = "ABCD"
    variable_range = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

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
    if args.seed:
        seed = args.seed
    if args.range:
        variable_range = args.range

    #Can I get a switch statement please?
    if args.argLength:
        argLengthTuple = pinLength(pinLocation,libraryLocation,args.file,count,arg=True)
        print("[+] Found Num {} : Count {}".format(argLengthTuple[0], argLengthTuple[1]))

    if args.inputLength:
        inputLengthTuple = pinLength(pinLocation,libraryLocation,args.file,count,arg=False)
        print("[+] Found Num {} : Count {}".format(inputLengthTuple[0], inputLengthTuple[1]))

    if args.arg:
        pattern = pinIter(pinLocation,libraryLocation,args.file,seed,variable_range,arg=True)
        print("[+] Found pattern {}".format(pattern))

    if args.input:
        pattern = pinIter(pinLocation,libraryLocation,args.file,seed,variable_range,arg=False)
        print("[+] Found pattern {}".format(pattern))



def readCount():
    inscountFileName = "inscount.out"
    inscountFile = open(inscountFileName)
    line = inscountFile.read()
    count = int(line.split(' ')[1])
    inscountFile.close()
    return count

def sendPinArgCommand(pin,library,binary,arg):
    COMMAND = "{}/pin -t {}/inscount0.so -- {} {}".format(pin,library,binary,arg)
    #os.popen(COMMAND)
    os.system(COMMAND)
    print(COMMAND)
    count = readCount()
    return count

def sendPinInputCommand(pin,library,binary,input):
    #TODO redo sending input
    COMMAND = "{}/pin -t {}/inscount0.so -- {} <<< \'{}\'".format(pin,library,binary,input)
    #os.popen(COMMAND)
    os.system(COMMAND)
    count = readCount()
    return count

def pinLength(pin,library,binary,length,arg=False):
    lengthDict = {}
    for i in range(length):
        if arg:
            count = sendPinArgCommand(pin,library,binary,'A'*(i+1))
        else:
            count = sendPinInputCommand(pin,library, binary, 'A' * (i + 1))
        lengthDict[i] = count

    #Get largest count value
    largestCount = 0
    largestNum = 0
    for num in lengthDict:
        if lengthDict[num] > largestCount:
            largestCount = lengthDict[num]
            largestNum = num
    return (largestNum,largestCount)

def pinIter(pin,library,binary,seed,variable_range,arg=False):

    seedLength = len(seed)

    for i in range(seedLength):
        rangeDict = {}
        for item in variable_range:
            #Exchange value in seed for our range values
            #Python strings can't do it, so we use a list
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
        for num in rangeDict:
            if rangeDict[num] > largestCount:
                largestCount = rangeDict[num]
                largestItem= num

        #Slot the value in
        seedList = list(seed)
        seedList[i] = largestItem
        seed = ''.join(seedList)
    return seed


main()