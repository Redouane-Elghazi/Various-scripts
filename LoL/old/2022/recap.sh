#!/bin/bash

python3 league_fullauto_overtime.py $1 2022 SPRING 60
python3 playoffs_overtime.py $1 2022 SPRING 60 76
./mergegif.sh $1
gifsicle -i $1/$1-recap-final.gif -O3 --colors 256 -o $1/$1-recap-final-256.gif
