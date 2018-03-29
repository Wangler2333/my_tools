#!/bin/sh

Dir=`dirname $0`

mkdir -p $Dir/temp

test -s $Dir/temp
if [ $? -eq 1 ];then 
   mkdir -p $Dir/temp
fi  