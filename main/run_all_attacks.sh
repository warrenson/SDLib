#!/bin/bash

#conda activate shilling

python main.py
perl -i -pne 's/average/bandwagon/g' ../config/*.conf

python main.py
perl -i -pne 's/bandwagon/hybrid/g' ../config/*.conf

python main.py

perl -i -pne 's/hybrid/love-hate/g' ../config/*.conf

python main.py
perl -i -pne 's/love-hate/random/g' ../config/*.conf

python main.py
perl -i -pne 's/random/reverse-bandwagon/g' ../config/*.conf

python main.py
# Return to start state
perl -i -pne 's/reverse-bandwagon/average/g' ../config/*.conf
