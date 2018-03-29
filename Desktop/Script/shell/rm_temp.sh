#!/bin/sh

Dir=`dirname $0`

rm -rf $Dir/temp

test -s $Dir/temp
if [ $? -eq 0 ];then 
   rm -rf $Dir/temp
fi   