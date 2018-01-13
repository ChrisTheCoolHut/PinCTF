# PinCTF

This tool is designed to use [Intel's Pin Tool](https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool) to instrument reverse engineering binaries and count instructions.

This tool is designed to use instruction counting as an avenue for [Side Channel Analysis](https://en.wikipedia.org/wiki/Side-channel_attack). By counting the number of instruction exeuted in a given reverse engineering program we can guess (Sometimes) that the more instructions that are executed per input, the closer we are to the flag.

## Install Pin
Included in this repo is a script for pulling down Intel's PIN and instructions for building it on Ubuntu 16.04. 

```
Instructions Here (./deps.sh)
```

## Running PinCTF
PinCTF is implemented as a python script wrapping PIN. It will execute a pin command then read from PIN's produced *inscount.out* file

```
[chris@Thor pinCTF]$ python pinCTF.py -h
usage: pinCTF.py [-h] [-f FILE] [-a] [-al] [-i] [-il] [-p PINLOCATION]
                 [-l PINLIBRARYLOCATION] [-c COUNT] [-s SEED] [-r RANGE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file to run pin against
  -a, --arg             Trace instructions for passed in argument
  -al, --argLength      Trace instructions for passed in argument length
  -i, --input           Trace instructions for given input
  -il, --inputLength    Trace instructions for input length
  -p PINLOCATION, --pinLocation PINLOCATION
                        Location of pin's directory
  -l PINLIBRARYLOCATION, --pinLibraryLocation PINLIBRARYLOCATION
                        Location of pin's instruction0.so libraries
  -c COUNT, --count COUNT
                        MaxLength to for length based pin
  -s SEED, --seed SEED  Initial seed for input or arg pin
  -r RANGE, --range RANGE
                        range of characters to iterate pin over
```
