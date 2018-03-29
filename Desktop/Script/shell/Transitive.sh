#!/bin/sh
#set -x 
Command_SH=`ls /Volumes/DATA/_Script`
for Some_One in $Command_SH
do 
cd /Volumes/DATA/_Script
chmod +x $Some_One
done

