# PinCTF

This tool is designed to use [Intel's Pin Tool](https://software.intel.com/en-us/articles/pin-a-dynamic-binary-instrumentation-tool) to instrument reverse engineering binaries and count instructions.

This tool is designed to use instruction counting as an avenue for [Side Channel Analysis](https://en.wikipedia.org/wiki/Side-channel_attack). By counting the number of instruction exeuted in a given reverse engineering program we can guess (Sometimes) that the more instructions that are executed per input, the closer we are to the flag.

## Install Pin
Included in this repo is a script for pulling down Intel's PIN and instructions for building it on Ubuntu 16.04. 

```
#This script will pull PIN and install dependencies needed.
./installPin.sh
```

## Running PinCTF
PinCTF is implemented as a python script wrapping PIN. It will execute a pin command then read from PIN's produced *inscount.out* file

```
[chris@Thor pinCTF]$  ./pinCTF.py -h
usage: pinCTF.py [-h] [-f FILE] [-a] [-al] [-i] [-il] [-p PINLOCATION]
                 [-l PINLIBRARYLOCATION] [-c COUNT] [-s SEED] [-r RANGE]
                 [-sl SEEDLENGTH] [-st SEEDSTART] [-t] [-tc THREADCOUNT]

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
  -sl SEEDLENGTH, --seedLength SEEDLENGTH
                        Initial seed length for input or arg pin
  -st SEEDSTART, --seedStart SEEDSTART
                        Initial seed index for pin
  -t, --threading       Enables threading
  -tc THREADCOUNT, --threadCount THREADCOUNT
                        Number of threads
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
Now we know we that the flag is 28 characters long and we can start looking for a flag of 28 characters.


Once you've found a length that seems to work you can use pin to change each value testing for instruction changes
The -sl flag can be used to determine the length of the initial seed, and the -r flag can be used to choose what range to iterate over
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

This process is pretty slow and can be sped up with threading. The -t (--threading) flag will enable threading and -tc represents the thread count

```
time ./pinCTF.py -f /home/chris/PinCTF/examples/crypt4 -a -sl 26 --threading -tc 4
[+] iter 0 using d for dAAAAAAAAAAAAAAAAAAAAAAAAA
[+] iter 1 using y for dyAAAAAAAAAAAAAAAAAAAAAAAA
[+] iter 2 using n for dynAAAAAAAAAAAAAAAAAAAAAAA
[+] iter 3 using 4 for dyn4AAAAAAAAAAAAAAAAAAAAAA
[+] iter 4 using m for dyn4mAAAAAAAAAAAAAAAAAAAAA
[+] iter 5 using 1 for dyn4m1AAAAAAAAAAAAAAAAAAAA
[+] iter 6 using c for dyn4m1cAAAAAAAAAAAAAAAAAAA
[+] iter 7 using a for dyn4m1caAAAAAAAAAAAAAAAAAA
[+] iter 8 using l for dyn4m1calAAAAAAAAAAAAAAAAA
[+] iter 9 using l for dyn4m1callAAAAAAAAAAAAAAAA
[+] iter 10 using y for dyn4m1callyAAAAAAAAAAAAAAA
[+] iter 11 using _ for dyn4m1cally_AAAAAAAAAAAAAA
[+] iter 12 using d for dyn4m1cally_dAAAAAAAAAAAAA
[+] iter 13 using 3 for dyn4m1cally_d3AAAAAAAAAAAA
[+] iter 14 using c for dyn4m1cally_d3cAAAAAAAAAAA
[+] iter 15 using r for dyn4m1cally_d3crAAAAAAAAAA
[+] iter 16 using y for dyn4m1cally_d3cryAAAAAAAAA
[+] iter 17 using p for dyn4m1cally_d3crypAAAAAAAA
[+] iter 18 using t for dyn4m1cally_d3cryptAAAAAAA
[+] iter 19 using 3 for dyn4m1cally_d3crypt3AAAAAA
[+] iter 20 using d for dyn4m1cally_d3crypt3dAAAAA
[+] iter 21 using _ for dyn4m1cally_d3crypt3d_AAAA
[+] iter 22 using c for dyn4m1cally_d3crypt3d_cAAA
[+] iter 23 using 0 for dyn4m1cally_d3crypt3d_c0AA
[+] iter 24 using d for dyn4m1cally_d3crypt3d_c0dA
[~] Largest instruction count found to match several others or very close
[~] Locating largest difference from average instead
[+] iter 25 using 3 for dyn4m1cally_d3crypt3d_c0d3
[+] Found pattern dyn4m1cally_d3crypt3d_c0d3

real	3m26.511s
user	10m53.012s
sys	2m21.344s
```
