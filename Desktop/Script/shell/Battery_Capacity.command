#!/bin/sh
#set -x
Check()
{
Max=`ypc2 -drk B0FC | sed 's/\..*//'`
Cur=`ypc2 -drk B0RM | sed 's/\..*//'`
Cap=$(expr $Cur "*" 100 / $Max)
}

Check
while [ $Cap -le "100" ]
do 
[ $Cap -ge "60" ] && echo "\033[032m Battery Capacity: $Cap% \033[030m"
[ $Cap -lt "60" ] && echo "\033[031m Battery Capacity: $Cap% \033[030m"
Check
sleep 1
done