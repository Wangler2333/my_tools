#!/bin/sh

Dir=`dirname $0`

expect -c "set timeout 2;spawn eos-ssh; expect -re \".*password*\";send \"controlbits read -a\r\";expect -re \"$\";interact" >> $Dir/CB_Status.txt