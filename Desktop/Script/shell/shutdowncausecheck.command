#!/bin/sh

cd /var/log
#cd /Users/vincent_jiang/Downloads/system

gunzip -d system*.gz
counter=`cat system.log* | grep "Previous shutdown cause: -128" | wc -l`
if ([ $counter -gt 0 ]); then
    echo "Get shutdown cause -128"
    exit 1
fi 
exit 0
