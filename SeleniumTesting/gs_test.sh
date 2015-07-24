#!/bin/bash

if [ ! -d "./report" ]; then
    mkdir "./report"
fi
folder="$(date +"%d-%m-%y")"
if [ ! -d "./report/$folder" ]; then
    mkdir "./report/$folder"
fi
filename="$(date +"%H.%M.%S").txt"
python ./source/GSchrome.py 2> "./report/$folder/$filename"