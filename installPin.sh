#!/bin/bash

WORKDIR=$(pwd)

#Pull latest from https://software.intel.com/en-us/articles/pin-a-binary-instrumentation-tool-downloads

URL=https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.7-97619-g0d0c92f4f-msvc-windows.zip

wget $URL -O pin.tar.gz 

tar -xvf pin.tar.gz

#Install Ubuntu Dependencies
sudo apt-get install gcc-multilib g++-multilib libc6-dev-i386

#Rename pin directory
mv pin-* pin

cd pin/source/tools/ManualExamples/

#Build for both 32 and 64 bit
make inscount0.test TARGET=ia32
make inscount0.test

#Move inscount.so libraries up to PinCTF's directory
mv obj-ia32 $WORKDIR/
mv obj-intel64 $WORKDIR/

#IPython used for debugging scripts
sudo apt install python3-pip
pip3 install ipython

#Setup config with defaults
printf "pin:%s
library:%s
count:%s
seed:%s" $WORKDIR/pin $WORKDIR/obj-ia32 20 ABCD > config
