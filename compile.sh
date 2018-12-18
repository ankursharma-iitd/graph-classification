#!/bin/bash

cd ./gaston-1.1-re
make clean
make
cp gaston ../
cp gaston ../part1
cd ..
cd ./libsvm-3.23
make clean
make
cp svm-predict ../
cp svm-train ../
