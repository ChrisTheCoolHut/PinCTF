# PinCTF

This tool is designed to use [Intel's Pin Tool](https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool) to instrument reverse engineering binaries and count instructions.

This tool is designed to use instruction counting as an avenue for [Side Channel Analysis](https://en.wikipedia.org/wiki/Side-channel_attack). By counting the number of instruction exeuted in a given reverse engineering program we can guess (Sometimes) that the more instructions that are executed per input, the closer we are to the flag.

## Install Pin
Included in this repo is a script for pulling down Intel's PIN and instructions for building it on Ubuntu 16.04. 

```
#This script will pull PIN and install dependencies needed.
./InstallPin.sh
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

To compare instruction counts to length use the -il or -al commands
The -c command is used to specifyhow many A's to test

```
./pinCTF.py -f examples/wyvern_c85f1be480808a9da350faaa6104a19b -il -l obj-intel64/ -c 30

Num  : Instr Count    AAAAAAAAAAAAAAAAAAA
1    : 2119788        
2    : 2119789        
3    : 2119789        
4    : 2119784        
5    : 2119788        
6    : 2119789        
7    : 2119791        
8    : 2119782        
9    : 2119786        
10   : 2119787        
11   : 2119791        
12   : 2119786        
13   : 2119790        
14   : 2119791        
15   : 2119818        
16   : 2119822        
17   : 2119826        
18   : 2119825        
19   : 2119831        
20   : 2119824        
21   : 2119830        
22   : 2119831        
23   : 2119835        
24   : 2119826        
25   : 2119830        
26   : 2119831        
27   : 2119835        
28   : 2132982        
29   : 2119834        
30   : 2119863        
[+] Found Num 28 : Count 2132982

```

Once you've found a length that seems to work you can use pin to change each value testing for instruction changes
The -sl flag can be used to determine the length, and the -r flag can be used to choose what range to iterate over
```
./pinCTF.py -f examples/wyvern_c85f1be480808a9da350faaa6104a19b -i -l obj-intel64/ -sl 28 -r abcdefghijklmnopqrstuvwxyz012345_-+LVMA
[+] iter 0 using d for dAAAAAAAAAAAAAAAAAAAAAAAAAAA
[+] iter 1 using r for drAAAAAAAAAAAAAAAAAAAAAAAAAA
[+] iter 2 using 4 for dr4AAAAAAAAAAAAAAAAAAAAAAAAA
[+] iter 3 using g for dr4gAAAAAAAAAAAAAAAAAAAAAAAA
[+] iter 4 using 0 for dr4g0AAAAAAAAAAAAAAAAAAAAAAA
[+] iter 5 using n for dr4g0nAAAAAAAAAAAAAAAAAAAAAA
[+] iter 6 using _ for dr4g0n_AAAAAAAAAAAAAAAAAAAAA
[+] iter 7 using o for dr4g0n_oAAAAAAAAAAAAAAAAAAAA
[+] iter 8 using r for dr4g0n_orAAAAAAAAAAAAAAAAAAA
[+] iter 9 using _ for dr4g0n_or_AAAAAAAAAAAAAAAAAA
[+] iter 10 using p for dr4g0n_or_pAAAAAAAAAAAAAAAAA
[+] iter 11 using 4 for dr4g0n_or_p4AAAAAAAAAAAAAAAA
[+] iter 12 using t for dr4g0n_or_p4tAAAAAAAAAAAAAAA
[+] iter 13 using r for dr4g0n_or_p4trAAAAAAAAAAAAAA
[+] iter 14 using i for dr4g0n_or_p4triAAAAAAAAAAAAA
[+] iter 15 using c for dr4g0n_or_p4tricAAAAAAAAAAAA
[+] iter 16 using 1 for dr4g0n_or_p4tric1AAAAAAAAAAA
[+] iter 17 using a for dr4g0n_or_p4tric1aAAAAAAAAAA
[+] iter 18 using n for dr4g0n_or_p4tric1anAAAAAAAAA
[+] iter 19 using _ for dr4g0n_or_p4tric1an_AAAAAAAA
[+] iter 20 using i for dr4g0n_or_p4tric1an_iAAAAAAA
[+] iter 21 using t for dr4g0n_or_p4tric1an_itAAAAAA
[+] iter 22 using 5 for dr4g0n_or_p4tric1an_it5AAAAA
[+] iter 23 using _ for dr4g0n_or_p4tric1an_it5_AAAA
[+] iter 24 using L for dr4g0n_or_p4tric1an_it5_LAAA
[+] iter 25 using L for dr4g0n_or_p4tric1an_it5_LLAA
[+] iter 26 using V for dr4g0n_or_p4tric1an_it5_LLVA
[+] iter 27 using M for dr4g0n_or_p4tric1an_it5_LLVM
[+] Found pattern dr4g0n_or_p4tric1an_it5_LLVM
```
