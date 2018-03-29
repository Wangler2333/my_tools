#!/bin/sh

Time=$(date "+%Y-%m-%d_%H-%M-%S")
Filename="m8_current_boot_$Time.log"
cat /Phoenix/Logs/m8_current_boot.log >> /Phoenix/Logs/$Filename