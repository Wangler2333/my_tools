#!/bin/bash

expect -c "spawn eos-ssh; expect \"# \"; send \"OSDToolbox bootargs -r burnin\r\"; expect \"# \"; send \"nvram -s\r\"; expect \"# \"; send \"nvram -p\r\"; expect \"# \"; send \"reboot\r\"; expect \"# \";"

