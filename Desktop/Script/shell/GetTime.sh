#!/bin/sh


time_get=`expect -c "set timeout 1;spawn ssh -l saseny 172.22.145.137 date +%H%M%S; expect -re \".*password*\";send \"SasenyZhou\r\";expect -re \"$\";interact"`
echo 
echo 
echo $time_get


