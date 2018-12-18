#!/bin/bash

#clone the GIT repo
git clone https://github.com/mehak126/graph-classification.git

#install the libraries used in python
pip3 install -U numpy scipy scikit-learn matplotlib networkx pickle multiprocessing functools 

#gaston binary will get compiled using gaston-1.1-re folder
#fsg binary is already linux compiled
#to allow the execution of 32-bit gspan binary on a 64-bit system
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386
sudo apt-get install multiarch-support
