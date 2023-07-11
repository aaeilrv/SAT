#!bin/sh

cd glucose-4.2.1/simp
make clean && make

cd ../../
python3 main.py $1