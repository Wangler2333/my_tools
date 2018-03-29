#!/bin/sh
#set -x 
rm -rf /Phoenix/Tables
sleep 1
cp -rf /Volumes/DATA/Tables/_Regression_Table/Run_in/None/Tables /Phoenix
sleep 1
/TE_Support/Tools/Phoenix/cleanup_Phoenix2.command
sleep 1
/TE_Support/Tools/Phoenix/cleanup_Phoenix2.command
sleep 1
#reboot