#!/bin/sh

Bundle_V=`ls /Phoenix/Tables | grep "PGQ" | awk -F '.tb*' '{print$1}'`
Bundle_Folder=`ls /Volumes/DATA/Regression_Log | grep -c "$Bundle_V"`
if [ $Bundle_Folder = 0 ];then 
mkdir /Volumes/DATA/Regression_Log/$Bundle_V
fi 