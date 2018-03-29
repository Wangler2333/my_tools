#!/bin/sh
#set -x
cd /
CM_Bundle=`ls *.dmg | awk -F '.dmg' '{print$1}'`
sleep 1
echo "\033[32m $CM_Bundle \033[30m"
touch /private/var/root/Desktop/$CM_Bundle