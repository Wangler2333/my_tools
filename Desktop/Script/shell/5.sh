#!/bin/bash 

time_limit=6
time_interval=1       

while [ "$SECONDS" -le "$time_limit" ]
do 
  if [ $SECONDS -lt 7 ]
  then 
     second=1
     let second+=1
  fi 
  echo "This script already running $SECONDS second(s)."
  sleep $time_interval
done

open -a /Applications/Apowersoft\ Screen\ Recorder.app

killall Recorder.app

exit 0     